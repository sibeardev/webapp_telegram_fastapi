from fastapi import APIRouter

from .routes import telegram, users, webapp

api_router = APIRouter()

api_router.include_router(telegram.router)
api_router.include_router(webapp.router)
api_router.include_router(users.router)
