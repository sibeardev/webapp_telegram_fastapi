import logging
from urllib.parse import urljoin

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update, WebAppInfo
from telegram.constants import ParseMode
from telegram.ext import CommandHandler, ContextTypes, filters

from bot.models import User
from core.config import EXTERNAL_URL

logger = logging.getLogger(__name__)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:

    user = await User.update_or_create(update.effective_user.to_dict())  # type: ignore
    url = urljoin(EXTERNAL_URL, "")
    buttons = [[InlineKeyboardButton("🚀 run WebApp", web_app=WebAppInfo(url))]]

    await update.message.reply_text(  # type: ignore
        text=f"Welcome, {user.username}!",
        parse_mode=ParseMode.HTML,
        reply_markup=InlineKeyboardMarkup(buttons),
    )


handlers = [CommandHandler("start", start, filters=filters.ChatType.PRIVATE)]
