import json
import logging
import os
import pathlib

logging.captureWarnings(True)
logger = logging.getLogger("telegram-loader")
logger.setLevel(logging.DEBUG)
logger.addHandler(logging.StreamHandler())

from pyspark.sql import DataFrame
from pyspark.sql.functions import from_json, col, map_from_entries
from pyspark.sql.functions import udf

from uwcip.sharedutils.fileutils import read_file

from lake_loader.base.loader import BaseLoader
from lake_loader.telegram.parser import TelegramParser


class TelegramLoader(BaseLoader):

    def __init__(self, spark, read_options, write_options):
        super().__init__(spark, read_options, write_options)
        self._parser = None

    def _get_parser_udf(self):

        parser = TelegramParser()

        def parse_message(msg):
            try:
                message = json.loads(msg)
                result = json.dumps(parser.parse_data(message))
                return result
            except Exception as e:
                logger.exception(e)
                return

        parse_message_udf = udf(lambda m: parse_message(m))
        return parse_message_udf

    def transform_stream(self, df: DataFrame):
        if self._parser is None:
            self._parser = self._get_parser_udf()

        schema_path = os.path.join(pathlib.Path(__file__).parent.resolve(), "schema/telegram_v1.json")
        schema = read_file(schema_path)  # load schema
        dft = (
            df.withColumn("headers", map_from_entries("headers").alias("headers"))
            .withColumn("collection", col("headers.collection").cast("string"))
            .withColumn("jstring", col("value").cast("string"))
            .withColumn("dat_gold", self._parser(col("jstring")))
            .withColumn("dat_json", from_json(col("dat_gold"), schema))
            .filter(col('dat_json').isNotNull())
            .select("collection", "dat_json.*")
        )

        return dft
