from beanie import init_beanie
from motor.motor_asyncio import AsyncIOMotorClient

from bot.models import User

from .config import MONGO_DSN


async def init_db():
    client = AsyncIOMotorClient(MONGO_DSN)
    db = client.ai_tracker
    await init_beanie(database=db, document_models=[User])  # type: ignore
