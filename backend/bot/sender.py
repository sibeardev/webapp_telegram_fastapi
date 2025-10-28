import logging
from telegram import error as tg_error
from bot.dispatcher import TELEGRAM_BOT

logger = logging.getLogger(__name__)


async def send_message(user_id: int, message_text: str) -> None:
    try:
        await TELEGRAM_BOT.bot.send_message(chat_id=user_id, text=message_text)

    except tg_error.Forbidden:
        logger.warning(
            f"Cannot send message to user {user_id}: Bot blocked or user deactivated"
        )
    except tg_error.BadRequest as e:
        logger.error(f"Bad request for user {user_id}: {e}", exc_info=True)
    except tg_error.TimedOut:
        logger.warning(
            f"Timeout while sending message to user {user_id}, retrying later"
        )
    except tg_error.NetworkError:
        logger.warning(f"Network error while sending message to user {user_id}")
    except tg_error.TelegramError as e:
        logger.error(f"Telegram error for user {user_id}: {e}", exc_info=True)
    except Exception as e:
        logger.error(
            f"Unexpected error sending message to user {user_id}: {e}", exc_info=True
        )
