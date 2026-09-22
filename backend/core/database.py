import os
from motor.motor_asyncio import AsyncIOMotorClient

class DataBase:
    client: AsyncIOMotorClient = None

db = DataBase()

async def connect_to_mongo():
    # Load from environment variable, fallback to localhost for development
    mongo_uri = os.getenv("MONGO_URI", "mongodb://localhost:27017")
    db.client = AsyncIOMotorClient(mongo_uri)
    print(f"Connected to MongoDB at {mongo_uri}")

async def close_mongo_connection():
    if db.client is not None:
        db.client.close()
        print("Closed MongoDB connection.")

def get_database():
    return db.client.bakery_db