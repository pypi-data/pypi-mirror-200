# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['lake_loader', 'lake_loader.base', 'lake_loader.telegram']

package_data = \
{'': ['*']}

install_requires = \
['confluent_kafka>=2.0.0,<3.0.0',
 'pyspark>=3.3.2,<4.0.0',
 'sharedutils>=1.1,<1.2']

entry_points = \
{'console_scripts': ['main = lake_loader.main:main']}

setup_kwargs = {
    'name': 'lake-loader',
    'version': '1.0.20230329232345',
    'description': '',
    'long_description': '# Datalake Loader\n\nCode under **lake-loader** consumes and transforms data from various online platforms and save them into azure datalake\nstorage. \n\n\n## Runtime Stages\nThis code has 4 runtime stages: *local_local*, *local_remote*, *remote_dev*, and *remote_prod*.\n\n### Local_Local\n\nThis runtime stage uses localhost spark; it consumes data from local kafka and writes the consumed data directly to\nconsole. This runtime setting doesn\'t rely on any azure computing services. To run this stage, first follow\nthe `README.md` file under `projects/local-setup` to set up local development environment.\n\n##### Telegram\n\nTo run telegram, first copy `lake-loader/sample_env_files/local_local.env.sample` to `lake-loader/.env` and modify the\nfile accordingly. Then, under `lake-loader` run `source .env` to export all environmental variables.\n\nNext run the following:\n\n```\npoetry run main telegram\n```\n\n### Local_Remote\n\nThis runtime stage uses localhost spark that connects to remote kafka and remote adls storage. It consumes data from\nazure eventhub kafka and writes to azure datalake storage. To run this stage, first obtain azure credentials for\neventhub and adls gen 2.\n\n#### Telegram\n\nTo run telegram, first copy `lake-loader/sample_env_files/local_remote.env.sample` to `lake-loader/.env` and modify the\nfile accordingly to fill out missing credentials. Then, under `lake-loader` run `source .env` to export all\nenvironmental variables.\n\nNext run the following:\n\n```\npoetry run main telegram\n```\n\n### Remote_Dev\n\nThis runtime stage runs `lake-loader` on databricks. First, fill out variables\nfrom `lake-loader/sample_env_files/remote_dev.env.sample` and then copy the variables to databrick\'s computing cluster.\nSee [Spark configuration](https://learn.microsoft.com/en-us/azure/databricks/clusters/configure). Next,\nrun `poetry build` under `lake-loader` to build a wheel. The wheel is under `lake-loader/dist` folder and has the\nname `lake_loader-x.y-py3-none-any.whl`. Next, create and run a\ndatabricks [job](https://docs.databricks.com/workflows/jobs/jobs.html) by uploading the wheel. See the following image to fill out the relevant fields. Note that if a wheel is updated, the old wheel needs to be removed from the computing cluster\'s libraries.\n\n![job](job_creation.png "job creation").\n\n## Schema\nSpark uses json schema when transforming raw data. The schema generation process is currently outside the `lake-loader` repo. Using telegram as an example, we first capture a hundred of raw telegram messages. We then use the telegram parser to transform the raw data into gold data. Next, we use spark to read the batch of transformed gold data to infer their schema. The schema is then written to file and dropped off to `lake-loader/schema/`. When the telegram parser is updated, the schema may also need to be updated (e.g. `schema/telegram_v1.json` needs to updated to `schema/telegram_v2.json`.',
    'author': 'Lia Bozarth',
    'author_email': 'liafan@uw.edu',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9',
}


setup(**setup_kwargs)
