from telegram import InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo

from app.settings import WEBHOOK_URL


def create_main_markup(user_id):
    buttons = [
        [
            InlineKeyboardButton(
                "WebApp", web_app=WebAppInfo(f"{WEBHOOK_URL}/user/{user_id}")
            )
        ]
    ]

    return InlineKeyboardMarkup(buttons)
