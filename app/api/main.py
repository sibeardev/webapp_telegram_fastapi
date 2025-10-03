from fastapi import APIRouter

from .routes import telegram

api_router = APIRouter()

api_router.include_router(telegram.router)
