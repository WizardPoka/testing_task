import logging
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.fsm.storage.memory import MemoryStorage
from pymongo import MongoClient
import os

API_TOKEN = os.getenv("TELEGRAM_API_TOKEN")
MONGO_URL = os.getenv("MONGO_URL", "mongodb://mongo:27017")

logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(storage=storage)

client = MongoClient(MONGO_URL)
db = client.message_db

async def send_welcome(message: types.Message):
    await message.reply("Hi!\nI'm MessageBot!\nUse /messages to see messages and /new to add a new message.")

async def list_messages(message: types.Message):
    messages = db.messages.find()
    count = db.messages.count_documents({})
    if count == 0:
        await message.reply("No messages yet.")
    else:
        response = "Messages:\n"
        for msg in messages:
            response += f"{msg['author']}: {msg['content']}\n"
        await message.reply(response)

async def new_message(message: types.Message):
    args = message.text.split(' ', 2)
    if len(args) != 3:
        await message.reply("Usage: /new <author> <message>")
    else:
        author, content = args[1], args[2]
        db.messages.insert_one({"author": author, "content": content})
        await message.reply("Message added!")

dp.message.register(send_welcome, Command(commands=["start", "help"]))
dp.message.register(list_messages, Command(commands=["messages"]))
dp.message.register(new_message, Command(commands=["new"]))

async def main():
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
