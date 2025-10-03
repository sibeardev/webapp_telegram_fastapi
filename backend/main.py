import asyncio
import logging
import os
from urllib.parse import urljoin

import uvicorn
from app.api.main import api_router
from app.core import db
from app.core.config import DEBUG, EXTERNAL_URL, HOST, PORT, TELEGRAM_SECRET
from app.exceptions import exception_handlers
from bot.dispatcher import TELEGRAM_BOT
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from telegram import Update
from telegram.error import NetworkError, TelegramError

logger = logging.getLogger(__name__)


async def main() -> None:
    await db.init_db()

    await TELEGRAM_BOT.bot.delete_webhook(drop_pending_updates=True)
    await TELEGRAM_BOT.bot.set_webhook(
        url=urljoin(EXTERNAL_URL, "/telegram/update"),
        allowed_updates=Update.ALL_TYPES,
        secret_token=TELEGRAM_SECRET,
    )
    logger.info(await TELEGRAM_BOT.bot.get_me())
    logger.info(await TELEGRAM_BOT.bot.get_webhook_info())

    app = FastAPI(debug=DEBUG, exception_handlers=exception_handlers)  # type: ignore
    app.include_router(api_router)

    frontend_dir = "./frontend/public"
    if not os.path.exists("./frontend/public"):
        raise RuntimeError(f"Frontend build directory does not exist: {frontend_dir}")
    app.mount("/", StaticFiles(directory=frontend_dir, html=True), name="frontend")

    web_server = uvicorn.Server(
        config=uvicorn.Config(
            app=app,
            port=PORT,
            use_colors=True,
            host=HOST,
        )
    )

    async with TELEGRAM_BOT:
        try:
            logger.info(await TELEGRAM_BOT.bot.get_me())
            logger.info(await TELEGRAM_BOT.bot.get_webhook_info())
            await TELEGRAM_BOT.start()
            await web_server.serve()
        except (NetworkError, TelegramError) as error:
            logger.error("Telegram API error: %s", error, exc_info=True)
        except OSError as error:
            logger.error("Server error (port or config issue): %s", error, exc_info=True)
        except asyncio.CancelledError:
            logger.info("Asyncio task cancelled, shutting down gracefully.")
            raise
        except KeyboardInterrupt:
            logger.info("Server stopped manually.")
        except Exception as error:
            logger.error("Unexpected error: %s", error, exc_info=True)
        finally:
            await TELEGRAM_BOT.stop()
            logger.info("Bot and web server stopped.")


if __name__ == "__main__":
    asyncio.run(main())
