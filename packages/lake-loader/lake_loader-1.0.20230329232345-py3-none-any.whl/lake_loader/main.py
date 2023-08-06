import argparse
import logging
import os
import pathlib
from logging import config as logging_config

from uwcip.sharedutils import loggingutils

logging.captureWarnings(True)
logging_config.dictConfig(
    loggingutils.get_logging_config(os.path.join(pathlib.Path(__file__).parent.resolve(), '../log_config.yaml')))


def run(platform):
    if platform == 'telegram':
        from lake_loader.telegram.loader import TelegramLoader
        loader = TelegramLoader.from_config(platform)
        loader.load()
    else:
        raise ValueError(f"the platform {platform} is currently not supported")


def main():
    parser = argparse.ArgumentParser(
        prog="lake-loader-main",
        formatter_class=argparse.RawTextHelpFormatter,
        description=__doc__,
    )

    parser.add_argument("platform", help="e.g., telegram, youtube, reddit")
    args = parser.parse_args()
    platform = args.platform
    run(platform)


if __name__ == '__main__':
    main()
