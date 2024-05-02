import logging

from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorCollection

from app.settings import MONGODB_URL, PROJECT_NAME

logger = logging.getLogger(__file__)


def get_db_collection(collection_name: str) -> AsyncIOMotorCollection:
    """
    Connects to the MongoDB server and returns the specified collection.

    Args:
        collection_name (str): The name of the collection to connect to.

    Returns:
        AsyncIOMotorCollection: The MongoDB collection object.

    """
    try:
        client = AsyncIOMotorClient(MONGODB_URL)
        db = client.get_database(PROJECT_NAME)
        collection = db.get_collection(collection_name)

        return collection
    except Exception as error_message:
        logger.error(f"Failed to connect to MongoDB {error_message}")
