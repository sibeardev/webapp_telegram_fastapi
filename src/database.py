import motor.motor_asyncio

from settings import MONGODB_URL, PROJECT_NAME

client = motor.motor_asyncio.AsyncIOMotorClient(MONGODB_URL)
db = client.get_database(PROJECT_NAME)
USERS = db.get_collection("users")
