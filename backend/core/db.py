from beanie import init_beanie
from motor.motor_asyncio import AsyncIOMotorClient

from bot.models import User
from core.config import MONGO_DSN, PROJECT_NAME


async def init_db():
    client = AsyncIOMotorClient(MONGO_DSN)
    db = client[PROJECT_NAME]
    await init_beanie(database=db, document_models=[User])  # type: ignore
