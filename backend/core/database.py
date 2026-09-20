from motor.motor_asyncio import AsyncIOMotorClient

class DataBase:
    client: AsyncIOMotorClient = None

db = DataBase()

async def connect_to_mongo():
    db.client = AsyncIOMotorClient("mongodb://localhost:27017")
    print("Connected to MongoDB.")

async def close_mongo_connection():
    if db.client is not None:
        db.client.close()
        print("Closed MongoDB connection.")

def get_database():
    return db.client.bakery_db