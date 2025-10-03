import logging.config
import os

from .env import EnvSettings

ENV = EnvSettings()  # type: ignore

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_NAME = ENV.PROJECT_NAME

DEBUG = ENV.DEBUG
EXTERNAL_URL = str(ENV.EXTERNAL_URL)
PORT = ENV.PORT
HOST = ENV.HOST
PROJECT_NAME = ENV.PROJECT_NAME

# TELEGRAM SETTINGS
TELEGRAM_TOKEN = ENV.TELEGRAM.TOKEN
BOT_ADMIN_IDS = ENV.TELEGRAM.ADMINS
TELEGRAM_SECRET = ENV.TELEGRAM.SECRET

MONGO_DSN = str(ENV.MONGO_DSN)

# LOGGING SETTINGS
ERROR_LOG_FILENAME = os.path.join(BASE_DIR, "logs/error.log")
os.makedirs(os.path.dirname(ERROR_LOG_FILENAME), exist_ok=True)
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "default": {
            "format": "%(asctime)s:%(levelname)s:%(message)s",
            "datefmt": "%Y-%m-%d %H:%M:%S",
        },
        "simple": {"format": "%(filename)s:%(lineno)d: - %(message)s"},
    },
    "handlers": {
        "logfile": {
            "class": "logging.handlers.RotatingFileHandler",
            "level": "ERROR",
            "filename": ERROR_LOG_FILENAME,
            "formatter": "default",
            "backupCount": 2,
        },
        "console": {
            "class": "logging.StreamHandler",
            "level": "DEBUG",
            "formatter": "simple",
            "stream": "ext://sys.stdout",
        },
    },
    "loggers": {
        PROJECT_NAME: {
            "level": "INFO",
            "handlers": ["console"],
            "propagate": False,
        },
    },
    "root": {"level": "INFO", "handlers": ["logfile", "console"]},
}

logging.config.dictConfig(LOGGING)
