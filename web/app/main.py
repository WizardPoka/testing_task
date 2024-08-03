from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from typing import List
from pymongo import MongoClient
from bson.objectid import ObjectId
import os

app = FastAPI()

MONGO_URL = os.getenv("MONGO_URL", "mongodb://mongo:27017")
client = MongoClient(MONGO_URL)
db = client.message_db

class Message(BaseModel):
    author: str
    content: str

class MessageInDB(Message):
    id: str

@app.get("/api/v1/messages/", response_model=List[MessageInDB])
def get_messages(skip: int = 0, limit: int = 10):
    messages = db.messages.find().skip(skip).limit(limit)
    return [{"id": str(message["_id"]), "author": message["author"], "content": message["content"]} for message in messages]

@app.post("/api/v1/message/", response_model=MessageInDB)
def create_message(message: Message):
    message_dict = message.dict()
    result = db.messages.insert_one(message_dict)
    message_dict["id"] = str(result.inserted_id)
    return message_dict
