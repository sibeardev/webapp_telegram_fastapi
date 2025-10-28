from telegram.ext import Application

from bot.handlers import start, member
from core.config import TELEGRAM_TOKEN

TELEGRAM_BOT = (
    Application.builder()
    .token(TELEGRAM_TOKEN.get_secret_value())
    .concurrent_updates(True)
    .updater(None)
    .build()
)


TELEGRAM_BOT.add_handlers(
    handlers=[
        *start.handlers,
        *member.handlers,
    ]
)
