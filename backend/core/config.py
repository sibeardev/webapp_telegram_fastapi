import logging.config
import os
from pathlib import Path

from .env import EnvSettings

ENV = EnvSettings()  # type: ignore

BASE_DIR = Path(__file__).resolve().parents[1]
FRONTEND_DIR = BASE_DIR / "frontend" / "build"

PROJECT_NAME = ENV.PROJECT_NAME

DEBUG = ENV.DEBUG
EXTERNAL_URL = str(ENV.EXTERNAL_URL)
PORT = ENV.PORT
HOST = ENV.HOST
PROJECT_NAME = ENV.PROJECT_NAME

SECRET_KEY = ENV.SECRET_KEY
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

# TELEGRAM SETTINGS
TELEGRAM_TOKEN = ENV.TELEGRAM.TOKEN
BOT_ADMIN_IDS = ENV.TELEGRAM.ADMINS
TELEGRAM_SECRET = ENV.TELEGRAM.SECRET

MONGO_DSN = str(ENV.MONGO_DSN)
RABBITMQ_URL = ENV.RABBITMQ.URL

# LOGGING SETTINGS
ERROR_LOG_FILENAME = BASE_DIR / "frontend" / "error.log"
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
