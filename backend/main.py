import asyncio
import logging
import os
from urllib.parse import urljoin

import uvicorn
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from telegram import Update
from telegram.error import NetworkError, TelegramError

from app.api.routes.main import api_router
from app.exceptions import exception_handlers
from bot.dispatcher import TELEGRAM_BOT
from core import db
from core.config import DEBUG, EXTERNAL_URL, FRONTEND_DIR, HOST, PORT, TELEGRAM_SECRET

logger = logging.getLogger(__name__)

if not DEBUG:
    logging.getLogger("httpx").setLevel(logging.WARNING)


async def main() -> None:
    await db.init_db()

    await TELEGRAM_BOT.bot.delete_webhook(drop_pending_updates=True)
    await TELEGRAM_BOT.bot.set_webhook(
        url=urljoin(EXTERNAL_URL, "/api/telegram/update"),
        allowed_updates=Update.ALL_TYPES,
        secret_token=TELEGRAM_SECRET.get_secret_value(),
    )
    logger.info(await TELEGRAM_BOT.bot.get_me())
    logger.info(await TELEGRAM_BOT.bot.get_webhook_info())

    app = FastAPI(debug=DEBUG, exception_handlers=exception_handlers)  # type: ignore
    app.include_router(api_router)

    if not os.path.exists(FRONTEND_DIR):
        raise RuntimeError(f"Frontend build directory does not exist: {FRONTEND_DIR}")
    app.mount("/", StaticFiles(directory=FRONTEND_DIR, html=True), name="frontend")

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
            logger.error(
                "Server error (port or config issue): %s", error, exc_info=True
            )
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
