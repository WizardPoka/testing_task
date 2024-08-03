from pymongo.database import Database
from bson import ObjectId

from .models import Message, User
from .schemas import MessageCreate, MessageResponse

def get_messages(db: Database):
    messages_collection = db["messages"]
    messages = messages_collection.find()
    return [MessageResponse(id=str(m["_id"]), content=m["content"], user=UserResponse(id=str(m["user"]["id"]), username=m["user"]["username"])) for m in messages]

def create_message(db: Database, message_data: MessageCreate) -> MessageResponse:
    users_collection = db["users"]
    messages_collection = db["messages"]

    user_data = users_collection.find_one({"_id": ObjectId(message_data.user_id)})
    if not user_data:
        return None

    user = User(id=user_data["_id"], username=user_data["username"])

    new_message = Message(id=ObjectId(), content=message_data.content, user=user)
    messages_collection.insert_one({
        "_id": new_message.id,
        "content": new_message.content,
        "user": {
            "id": user.id,
            "username": user.username
        }
    })

    return MessageResponse(id=str(new_message.id), content=new_message.content, user=UserResponse(id=str(user.id), username=user.username))
