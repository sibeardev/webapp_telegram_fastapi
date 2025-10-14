from telegram.ext import Application

from bot.handlers import start
from core.config import TELEGRAM_TOKEN

TELEGRAM_BOT = (
    Application.builder()
    .token(TELEGRAM_TOKEN)
    .concurrent_updates(True)
    .updater(None)
    .build()
)


TELEGRAM_BOT.add_handlers(handlers=[*start.handlers])
