import logging

from app.core.config import TELEGRAM_TOKEN
from app.core.security import validate_telegram_init_data
from bot.models import User
from fastapi import APIRouter, HTTPException, Request

logger = logging.getLogger(__name__)

router = APIRouter(tags=["user"], prefix="/api/user")


@router.post("/auth")
async def webapp_auth(request: Request):
    data = await request.json()
    init_data = data.get("initData")
    init_data_unsafe = data.get("initDataUnsafe")

    if not init_data or not init_data_unsafe:
        raise HTTPException(status_code=400, detail="Invalid data")

    if not validate_telegram_init_data(init_data, TELEGRAM_TOKEN):
        raise HTTPException(status_code=403, detail="Invalid Telegram signature")

    user_data = init_data_unsafe.get("user")
    user = await User.update_or_create(user_data)

    return user
