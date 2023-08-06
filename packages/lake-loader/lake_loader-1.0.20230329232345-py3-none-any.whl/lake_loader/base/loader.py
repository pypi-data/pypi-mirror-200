import logging
from abc import ABC, abstractmethod

from pyspark.sql import DataFrame
from pyspark.sql import SparkSession

from uwcip.sharedutils.configutils import get_config

logger = logging.getLogger("base-loader")
logging.captureWarnings(True)
logger.setLevel(logging.DEBUG)
logger.addHandler(logging.StreamHandler())


def _get_dbutils(spark):
    runtime_stage = get_config("RUNTIME_STAGE")
    if runtime_stage == 'local_local' or runtime_stage == 'local_remote':
        return  # none
    try:
        from pyspark.dbutils import DBUtils
        dbutils = DBUtils(spark)
    except ImportError:
        import IPython
        dbutils = IPython.get_ipython().user_ns["dbutils"]
    return dbutils


def _get_spark_session(platform):
    runtime_stage = get_config("RUNTIME_STAGE")
    spark_builder = SparkSession.builder
    if runtime_stage == 'local_local' or runtime_stage == 'local_remote':
        spark = spark_builder.config('spark.jars.packages',
                                     'org.apache.spark:spark-sql-kafka-0-10_2.12:3.0.1,org.apache.hadoop:hadoop-azure:3.3.1').appName(
            f"local-spark-{platform}").getOrCreate()
    else:  # running remotely
        spark = spark_builder.appName(f"remote-spark-{platform}").getOrCreate()
    return spark


def _get_kafka_read_config(dbutils, platform):
    runtime_stage = get_config("RUNTIME_STAGE")
    kafka_topic = get_config(f"KAFKA_{platform.upper()}_TOPIC")
    read_options = {
        "subscribe": kafka_topic,
        "kafka.bootstrap.servers": get_config("KAFKA_BOOTSTRAP_SERVERS"),
        "kafka.sasl.mechanism": "PLAIN",
        "kafka.security.protocol": get_config("KAFKA_SECURITY_PROTOCOL"),
        "kafka.request.timeout.ms": "10000",
        "kafka.session.timeout.ms": "10000",
        "auto.offset.reset": "earliest",
        "includeHeaders": "true",
        "kafkaConsumer.pollTimeoutMs": "120000",
        "minOffsetsPerTrigger": "10"  # 10 messages minimum per batch
    }

    try:
        if runtime_stage == 'local_local':
            jaas = None
        elif runtime_stage == 'local_remote':
            username = get_config("KAFKA_SASL_USERNAME")
            password = get_config("KAFKA_SASL_PASSWORD")
            jaas = f"org.apache.kafka.common.security.plain.PlainLoginModule required username=\"{username}\" password=\"{password}\";"
        elif runtime_stage == 'remote_dev':
            username = dbutils.secrets.get('default-scope', 'kafka-sasl-username')
            password = dbutils.secrets.get("default-scope", 'kafka-sasl-password')
            jaas = f"kafkashaded.org.apache.kafka.common.security.plain.PlainLoginModule required username=\"{username}\" password=\"{password}\";"
        elif runtime_stage == 'remote_prod':
            username = dbutils.secrets.get('prod-scope', 'kafka-sasl-username')
            password = dbutils.secrets.get("prod-scope", 'kafka-sasl-password')
            jaas = f"kafkashaded.org.apache.kafka.common.security.plain.PlainLoginModule required username=\"{username}\" password=\"{password}\";"
        else:
            raise ValueError(f"runtime stage {runtime_stage} is not supported")
        if jaas:
            read_options["kafka.sasl.jaas.config"] = jaas  # set kafka username and password
    except ValueError as e:
        logger.exception(
            f"missing environmental variables (secrets) for kafka jass config for runtime stage {runtime_stage}")
        raise e

    read_config = {
        "format": "kafka",
        "options": read_options
    }
    logger.debug(f'read_config {read_config}')
    return read_config


def _get_kafka_write_config(spark, dbutils, platform):
    runtime_stage = get_config("RUNTIME_STAGE")
    try:
        if runtime_stage == 'local_local':
            return {}  # no write config
        elif runtime_stage == 'local_remote':
            account = get_config('AZURE_STORAGE_ACCOUNT_NAME')
            key = get_config("AZURE_STORAGE_ACCOUNT_KEY")
        elif runtime_stage == 'remote_dev':
            account = dbutils.secrets.get('default-scope', 'azure-storage-account-name')
            key = dbutils.secrets.get("default-scope", 'azure-storage-account-key')
        elif runtime_stage == 'remote_prod':
            account = dbutils.secrets.get('prod-scope', 'azure-storage-account-name')
            key = dbutils.secrets.get("prod-scope", 'azure-storage-account-key')
        else:
            raise ValueError(f"runtime stage {runtime_stage} is not supported")

        spark.conf.set(account, key)  # credentials to connect to adls

        kafka_topic = get_config(f"KAFKA_{platform.upper()}_TOPIC")
        checkpoint = f"{get_config('AZURE_STORAGE_BASE_PATH')}/{platform}/{kafka_topic}/checkpoint/"
        data_path = f"{get_config('AZURE_STORAGE_BASE_PATH')}/{platform}/{kafka_topic}/data/"

        write_options = {
            "checkpointLocation": checkpoint,
            "path": data_path,
            "failOnDataLoss": "true"
        }

        partitioned_by = [x.strip() for x in get_config(f"KAFKA_{platform.upper()}_PARTITION_BY").split(",")]
        write_config = {
            "format": get_config("AZURE_STORAGE_WRITE_FORMAT"),  # delta, json, parquet, etc. TODO change to delta
            "output_mode": "append",
            "partition_by": partitioned_by,
            "options": write_options
        }
        logger.debug(f'write_config {write_config}')
        return write_config
    except ValueError as e:
        logger.exception(f"missing environmental variables (secrets) for adls for runtime stage {runtime_stage}")
        raise e


class BaseLoader(ABC):

    @classmethod
    def from_config(cls, platform):
        spark = _get_spark_session(platform)
        dbutils = _get_dbutils(spark)

        # get kafka readstream options
        read_option = _get_kafka_read_config(dbutils, platform)

        # get kafka writestream (storage) options
        write_option = _get_kafka_write_config(spark, dbutils, platform)

        return cls(spark, read_option, write_option)

    def __init__(self, spark: SparkSession, read_options, write_options):
        self._spark = spark
        self._read_options = read_options
        self._write_options = write_options

    def read_stream(self) -> DataFrame:
        df = self._spark.readStream \
            .format(self._read_options['format']) \
            .options(**self._read_options['options']) \
            .load()
        return df

    def write_stream(self, df: DataFrame):
        if self._write_options:
            df.writeStream \
                .format(self._write_options['format']) \
                .outputMode(self._write_options['output_mode']) \
                .partitionBy(*self._write_options['partition_by']) \
                .options(**self._write_options['options']) \
                .start() \
                .awaitTermination()
        else:  # write to console
            df.writeStream \
                .format("console") \
                .outputMode("append") \
                .start() \
                .awaitTermination()

    def load(self):
        df = self.read_stream()
        df = self.transform_stream(df)
        self.write_stream(df)

    @abstractmethod
    def transform_stream(self, df: DataFrame):
        pass
