from telegram import Update, ChatMemberUpdated
from telegram.ext import ContextTypes, ChatMemberHandler
import logging
from bot.models import User

logger = logging.getLogger(__name__)


async def handle_chat_member(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.my_chat_member:
        return
    chat_member: ChatMemberUpdated = update.my_chat_member
    new_status = chat_member.new_chat_member.status
    user = await User.find_one(User.user_id == update.effective_user.id)
    if not user:
        return

    if new_status == "kicked":
        user.allows_write_to_pm = False

    elif new_status == "member":
        user.allows_write_to_pm = True

    await user.save()


handlers = [ChatMemberHandler(handle_chat_member)]
