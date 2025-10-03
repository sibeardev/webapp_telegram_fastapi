import logging
from datetime import datetime
from urllib.parse import urljoin

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update, WebAppInfo
from telegram.constants import ParseMode
from telegram.ext import CommandHandler, ContextTypes, filters

from app.core.config import EXTERNAL_URL
from bot.models import User

logger = logging.getLogger(__name__)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    tg_user = update.effective_user

    user = await User.find_one(User.user_id == tg_user.id)

    if not user:
        user = User(
            user_id=tg_user.id,
            username=tg_user.username,
            first_name=tg_user.first_name,
            last_name=tg_user.last_name,
            language_code=tg_user.language_code,
            is_premium=getattr(tg_user, "is_premium", False),
            allows_write_to_pm=getattr(tg_user, "allows_write_to_pm", True),
            photo_url=None,
            date_joined=datetime.now(),
            last_login=datetime.now(),
        )
        await user.insert()

    url = urljoin(EXTERNAL_URL, "bot/auth/")
    buttons = [[InlineKeyboardButton("🚀 run WebApp", web_app=WebAppInfo(url))]]

    await update.message.reply_text(  # type: ignore
        text=f"Welcome, {user.username}!",
        parse_mode=ParseMode.HTML,
        reply_markup=InlineKeyboardMarkup(buttons),
    )


handlers = [CommandHandler("start", start, filters=filters.ChatType.PRIVATE)]
