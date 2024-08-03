from pymongo import MongoClient

MONGO_URI = "mongodb://mongo:27017"
DATABASE_NAME = "message_db"

client = MongoClient(MONGO_URI)
db = client[DATABASE_NAME]

def get_db():
    return db

def init_db():
    users_collection = db["users"]
    users_collection.update_one(
        {"username": "admin"},
        {"$setOnInsert": {"_id": ObjectId(), "username": "admin"}},
        upsert=True
    )
