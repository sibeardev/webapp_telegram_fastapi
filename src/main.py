import asyncio
import logging.config
from warnings import filterwarnings

import uvicorn
from fastapi import FastAPI
from fastapi.requests import Request
from fastapi.responses import Response
from fastapi.staticfiles import StaticFiles
from starlette.routing import Mount, Route
from telegram import Update
from telegram.ext import Application
from telegram.warnings import PTBUserWarning

from exceptions import exception_handlers
from handlers.start import start
from routers import users
from settings import LOGGING_CONFIG, PORT, TELEGRAM_TOKEN, WEBHOOK_URL

logging.config.dictConfig(LOGGING_CONFIG)
logger = logging.getLogger(__file__)
filterwarnings(
    action="ignore", message=r".*CallbackQueryHandler", category=PTBUserWarning
)


async def main() -> None:
    # Create a Telegram application instance
    telegram_app = (
        Application.builder()
        .token(TELEGRAM_TOKEN)
        .concurrent_updates(True)
        .updater(None)
        .build()
    )
    # Setup Telegram update handlers
    start.setup_handler(telegram_app)
    # Set webhook URL for Telegram bot
    await telegram_app.bot.set_webhook(url=f"{WEBHOOK_URL}/telegram_update")

    async def telegram(request: Request) -> Response:
        """Define endpoint for receiving Telegram updates"""
        await telegram_app.update_queue.put(
            Update.de_json(data=await request.json(), bot=telegram_app.bot)
        )
        return Response()

    # Define routes for FastAPI application
    routes = [
        Route(path="/telegram_update", endpoint=telegram, methods=["POST"]),
        Mount(path="/static", app=StaticFiles(directory="static"), name="static"),
    ]
    app = FastAPI(debug=True, routes=routes, exception_handlers=exception_handlers)

    # Include others router
    app.include_router(users.router)

    # Create a uvicorn server instance
    web_server = uvicorn.Server(
        config=uvicorn.Config(
            app=app,
            port=PORT,
            use_colors=True,
            host="127.0.0.1",
        )
    )

    # Run Telegram application and web server concurrently
    async with telegram_app:
        await telegram_app.start()  # Start receiving Telegram updates
        await web_server.serve()  # Start serving FastAPI application
        await telegram_app.stop()  # Stop receiving Telegram updates


if __name__ == "__main__":
    asyncio.run(main())
