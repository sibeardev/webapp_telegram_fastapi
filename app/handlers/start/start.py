import logging

from telegram import Update, User, UserProfilePhotos
from telegram.ext import Application, CommandHandler, ContextTypes

from app.db.mongo import get_db_collection
from app.models.users import UserModel


from .keyboards import create_main_markup

logger = logging.getLogger(__file__)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    This function is the handler for the 'start' command in a Telegram bot.
    It is called when a user sends the '/start' command to the bot.

    Parameters:
    - update (telegram.Update): The update object containing information about the incoming message.
    - context (telegram.ext.ContextTypes.DEFAULT_TYPE): The context object containing additional information and functionality for the bot.

    Returns:
    - None

    Raises:
    - Any exception that occurs during the execution of the function.

    Functionality:
    1. Retrieves the user object from the update.
    2. Retrieves the user's profile photos using the Telegram bot API.
    3. If the user has profile photos, downloads the latest photo and saves it to a custom path.
    4. If the user does not have profile photos, uses a default photo.
    5. Creates a new UserModel object with the user's information.
    6. Updates the user's information in the USERS collection of the database.
    7. Sends a reply message to the user with a greeting and a custom keyboard markup.

    """
    try:
        tg_user: User = update.effective_user

        photos: UserProfilePhotos = await context.bot.get_user_profile_photos(tg_user.id)
        if photos:
            new_file = await context.bot.get_file(photos.photos[0][-1].file_id)
            photo_path = f"avatars/user_{tg_user.id}_photo.jpg"
            await new_file.download_to_drive(custom_path="static/" + photo_path)
        else:
            photo_path = "avatars/goose.jpg"

        new_user = UserModel(
            user_id=tg_user.id,
            username=tg_user.first_name,
            photo_url=photo_path,
        )
        await get_db_collection("users").find_one_and_update(
            {"user_id": tg_user.id},
            {"$set": new_user.model_dump(by_alias=True, exclude=["id"])},
            upsert=True,
        )
        await update.message.reply_text(
            f"Hi, {tg_user.first_name}",
            reply_markup=create_main_markup(tg_user.id),
        )
    except Exception as error_message:
        logging.error(f"An error occurred: {error_message}")


def setup_handler(application: Application) -> None:
    application.add_handler(CommandHandler(command="start", callback=start))
