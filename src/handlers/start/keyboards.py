from telegram import InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo

from settings import WEBHOOK_URL


def create_main_markup(user_id):
    buttons = [
        [
            InlineKeyboardButton(
                "WebApp", web_app=WebAppInfo(f"{WEBHOOK_URL}/users/{user_id}")
            )
        ]
    ]

    return InlineKeyboardMarkup(buttons)
