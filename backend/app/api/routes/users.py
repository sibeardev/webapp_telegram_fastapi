import logging

from fastapi import APIRouter, Depends, HTTPException, Request

from app.api.depends import get_current_user
from bot.models import User
from core.config import TELEGRAM_TOKEN
from core.security import create_access_token, validate_telegram_init_data

logger = logging.getLogger(__name__)

router = APIRouter(tags=["user"], prefix="/user")


@router.get("/me")
async def get_user(user: User = Depends(get_current_user)):
    return user


@router.post("/auth")
async def webapp_auth(request: Request):
    data = await request.json()
    init_data = data.get("initData")
    init_data_unsafe = data.get("initDataUnsafe")

    if not init_data or not init_data_unsafe:
        raise HTTPException(status_code=400, detail="Invalid data")

    if not validate_telegram_init_data(init_data, TELEGRAM_TOKEN.get_secret_value()):
        raise HTTPException(status_code=403, detail="Invalid Telegram signature")

    user_data = init_data_unsafe.get("user")
    user = await User.update_or_create(user_data)
    token = create_access_token(user.id)  # type: ignore

    return token
