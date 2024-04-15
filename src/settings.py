import os

from environs import Env
from fastapi.templating import Jinja2Templates

# Load environment variables
env = Env()
env.read_env()

# Define base directory and project name
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_NAME = env.str("PROJECT_NAME", "webapp_telegram_fastapi")

# Telegram Bot token, webhook URL, port, and debug mode
TELEGRAM_TOKEN = env.str("TELEGRAM_TOKEN")
WEBHOOK_URL = env.str("WEBHOOK_URL")
PORT = env.int("PORT", 8000)
DEBUG = env.bool("DEBUG", True)
X_TOKEN = env.str("X_TOKEN")

# Jinja2 templates directory
TEMPLATES = Jinja2Templates(directory="templates")

# MongoDB URL
MONGODB_URL = env.str("MONGODB_URL")

# Error log filename
ERROR_LOG_FILENAME = "error.log"

# Logging configuration
LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "default": {
            "format": "%(asctime)s:c:%(process)d:%(lineno)d "
            "%(levelname)s %(message)s",
            "datefmt": "%Y-%m-%d %H:%M:%S",
        },
        "simple": {
            "format": "%(filename)s:%(lineno)d: - %(message)s",
        },
    },
    "handlers": {
        "logfile": {
            "class": "logging.handlers.RotatingFileHandler",
            "level": "ERROR",
            "filename": ERROR_LOG_FILENAME,
            "formatter": "default",
            "backupCount": 2,
        },
        "verbose_output": {
            "class": "logging.StreamHandler",
            "level": "DEBUG",
            "formatter": "simple",
            "stream": "ext://sys.stdout",
        },
    },
    "loggers": {
        PROJECT_NAME: {
            "level": "INFO",
            "handlers": [
                "verbose_output",
            ],
            "propagate": False,
        },
    },
    "root": {"level": "INFO", "handlers": ["logfile", "verbose_output"]},
}
