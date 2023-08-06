import logging.config

import yaml
from haggis.logs import add_logging_level

from mimeo import utils

from .filters import DetailedFilter, RegularFilter


def setup_logging():
    add_logging_level("FINE", logging.DEBUG - 1)
    with utils.get_resource("logging.yaml") as config_file:
        config = yaml.safe_load(config_file.read())
        logging.config.dictConfig(config)
