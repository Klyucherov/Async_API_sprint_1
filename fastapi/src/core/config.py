import os
from logging import config as logging_config

from core.configs import ConnectionConfig, LogConfig
from core.logger import LOGGING

logging_config.dictConfig(LOGGING)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

CONNECTION_SETTINGS = ConnectionConfig()
LOG_SETTINGS = LogConfig()
