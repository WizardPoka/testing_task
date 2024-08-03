import logging
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.fsm.storage.memory import MemoryStorage
from pymongo import MongoClient
import os

# Получаем токен для Telegram API и URL для подключения к MongoDB из переменных окружения
API_TOKEN = os.getenv("TELEGRAM_API_TOKEN")
MONGO_URL = os.getenv("MONGO_URL", "mongodb://mongo:27017")

# Устанавливаем уровень логирования
logging.basicConfig(level=logging.INFO)

# Инициализируем бота, диспетчер и подключение к базе данных
bot = Bot(token=API_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(storage=storage)

# Подключаемся к MongoDB и выбираем базу данных и коллекцию
client = MongoClient(MONGO_URL)
db = client.message_db

async def send_welcome(message: types.Message):
    """Приветственное сообщение при запуске бота."""
    await message.reply(
        "Hi!\nI'm MessageBot!\n"
        "Use /messages to see messages.\n"
        "Send any message to save it."
    )

async def list_messages(message: types.Message):
    """Команда для вывода всех сохраненных сообщений."""
    messages = db.messages.find()
    count = db.messages.count_documents({})
    
    if count == 0:
        await message.reply("No messages yet.")
    else:
        response = "Messages:\n"
        for msg in messages:
            # Выводим автора и содержание сообщения
            response += f"{msg['author']}: {msg['content']}\n"
        await message.reply(response)

async def save_message(message: types.Message):
    """Сохраняем сообщение в базе данных и фиксируем отправителя."""
    # Определяем автора сообщения, используя имя пользователя Telegram
    author = message.from_user.username or f"User_{message.from_user.id}"
    content = message.text
    
    # Добавляем сообщение в базу данных
    db.messages.insert_one({"author": author, "content": content})
    
    # Подтверждаем сохранение сообщения
    await message.reply("Your message has been saved!")

# Регистрируем команды и обработчики сообщений
dp.message.register(send_welcome, Command(commands=["start", "help"]))
dp.message.register(list_messages, Command(commands=["messages"]))

# Для обработки всех сообщений, кроме команд, нужно использовать фильтр, который не включает в себя командные сообщения.
dp.message.register(save_message)

async def main():
    """Запуск процесса polling для получения обновлений от Telegram."""
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
