from telegram.ext import Application

from app.core.config import TELEGRAM_TOKEN

from .handlers import start

TELEGRAM_BOT = (
    Application.builder()
    .token(TELEGRAM_TOKEN)
    .concurrent_updates(True)
    .updater(None)
    .build()
)


TELEGRAM_BOT.add_handlers(handlers=[*start.handlers])
