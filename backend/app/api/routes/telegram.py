import asyncio
import json
import logging
import traceback

from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import JSONResponse
from telegram import Update
from telegram.error import TelegramError

from bot.dispatcher import TELEGRAM_BOT
from core.config import TELEGRAM_SECRET

logger = logging.getLogger(__name__)

router = APIRouter(tags=["telegram"], prefix="/telegram")


@router.post("/update")
async def telegram_update(request: Request):

    token = request.headers.get("X-Telegram-Bot-Api-Secret-Token")
    if token != TELEGRAM_SECRET.get_secret_value():
        logger.warning("Webhook request with invalid secret token")
        raise HTTPException(status_code=403, detail="Forbidden")

    try:
        data = await request.json()
        update = Update.de_json(data=data, bot=TELEGRAM_BOT.bot)
        await TELEGRAM_BOT.update_queue.put(update)

    except json.JSONDecodeError as error:
        logger.warning("Invalid JSON in webhook: %s", error, exc_info=True)
        return JSONResponse(
            {"ok": False, "error": "Invalid JSON"},
            status_code=400,
        )

    except (KeyError, TypeError, ValueError, TelegramError) as error:
        logger.warning("Failed to parse Telegram update: %s", error, exc_info=True)
        return JSONResponse(
            {"ok": False, "error": "Invalid Telegram update"},
            status_code=400,
        )

    except asyncio.QueueFull as error:
        logger.error("Update queue is full: %s", error, exc_info=True)
        return JSONResponse(
            {"ok": False, "error": "Queue full"},
            status_code=503,
        )

    except Exception:
        logger.error("Unexpected webhook error:\n%s", traceback.format_exc())
        return JSONResponse(
            {"ok": False, "error": "Internal server error"},
            status_code=500,
        )

    return JSONResponse(content={"ok": True})
