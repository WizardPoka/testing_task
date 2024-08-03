from pydantic import BaseModel
from bson import ObjectId

class UserBase(BaseModel):
    username: str

class UserCreate(UserBase):
    pass

class UserResponse(UserBase):
    id: str

class MessageBase(BaseModel):
    content: str

class MessageCreate(MessageBase):
    user_id: str

class MessageResponse(MessageBase):
    id: str
    user: UserResponse
