from bson import ObjectId
from typing import Optional

class User:
    def __init__(self, id: ObjectId, username: str):
        self.id = id
        self.username = username

class Message:
    def __init__(self, id: ObjectId, content: str, user: User):
        self.id = id
        self.content = content
        self.user = user
