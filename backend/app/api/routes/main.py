from fastapi import APIRouter

from app.api.routes import telegram, users

api_router = APIRouter(prefix="/api")

api_router.include_router(telegram.router)
api_router.include_router(users.router)
