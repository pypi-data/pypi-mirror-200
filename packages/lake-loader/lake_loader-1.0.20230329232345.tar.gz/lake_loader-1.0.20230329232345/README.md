# Datalake Loader

Code under **lake-loader** consumes and transforms data from various online platforms and save them into azure datalake
storage. 


## Runtime Stages
This code has 4 runtime stages: *local_local*, *local_remote*, *remote_dev*, and *remote_prod*.

### Local_Local

This runtime stage uses localhost spark; it consumes data from local kafka and writes the consumed data directly to
console. This runtime setting doesn't rely on any azure computing services. To run this stage, first follow
the `README.md` file under `projects/local-setup` to set up local development environment.

##### Telegram

To run telegram, first copy `lake-loader/sample_env_files/local_local.env.sample` to `lake-loader/.env` and modify the
file accordingly. Then, under `lake-loader` run `source .env` to export all environmental variables.

Next run the following:

```
poetry run main telegram
```

### Local_Remote

This runtime stage uses localhost spark that connects to remote kafka and remote adls storage. It consumes data from
azure eventhub kafka and writes to azure datalake storage. To run this stage, first obtain azure credentials for
eventhub and adls gen 2.

#### Telegram

To run telegram, first copy `lake-loader/sample_env_files/local_remote.env.sample` to `lake-loader/.env` and modify the
file accordingly to fill out missing credentials. Then, under `lake-loader` run `source .env` to export all
environmental variables.

Next run the following:

```
poetry run main telegram
```

### Remote_Dev

This runtime stage runs `lake-loader` on databricks. First, fill out variables
from `lake-loader/sample_env_files/remote_dev.env.sample` and then copy the variables to databrick's computing cluster.
See [Spark configuration](https://learn.microsoft.com/en-us/azure/databricks/clusters/configure). Next,
run `poetry build` under `lake-loader` to build a wheel. The wheel is under `lake-loader/dist` folder and has the
name `lake_loader-x.y-py3-none-any.whl`. Next, create and run a
databricks [job](https://docs.databricks.com/workflows/jobs/jobs.html) by uploading the wheel. See the following image to fill out the relevant fields. Note that if a wheel is updated, the old wheel needs to be removed from the computing cluster's libraries.

![job](job_creation.png "job creation").

## Schema
Spark uses json schema when transforming raw data. The schema generation process is currently outside the `lake-loader` repo. Using telegram as an example, we first capture a hundred of raw telegram messages. We then use the telegram parser to transform the raw data into gold data. Next, we use spark to read the batch of transformed gold data to infer their schema. The schema is then written to file and dropped off to `lake-loader/schema/`. When the telegram parser is updated, the schema may also need to be updated (e.g. `schema/telegram_v1.json` needs to updated to `schema/telegram_v2.json`.