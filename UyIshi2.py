import asyncio
import logging
import sys

from os import getenv
import random

from aiogram import Bot, Dispatcher, html
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart, Command
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import Message
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from dotenv import load_dotenv
import re

import psycopg2

load_dotenv()

TOKEN = getenv("BOT_TOKEN")
DB_PASSWORD = getenv("DB_PASSWORD")

dp = Dispatcher(storage=MemoryStorage())

class User:
    def __init__(self, first_name, last_name, email, chat_id):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.chat_id = chat_id


class Database:
    conn = psycopg2.connect(user="postgres", password=DB_PASSWORD, host="localhost", database="tg_bot", port=5432)
    @classmethod
    def add_user(cls, first_name, last_name, email, chat_id):
        curr = cls.conn.cursor()
        query = """INSERT INTO users(first_name, last_name, email, chat_id)
        VALUES(%s, %s, %s, %s);"""
        with cls.conn:
            curr.execute(query, (first_name, last_name, email, chat_id))

    @classmethod
    def search_user_by_chat_id(cls, chat_id):
        curr = cls.conn.cursor()
        query = """SELECT first_name, last_name, email, chat_id FROM users WHERE chat_id = %s;"""
        with cls.conn:
            curr.execute(query, (chat_id, ))
            user = curr.fetchone()
        if user is None:
            return None
        return User(*user)

    @classmethod
    def count_users(cls):
        curr = cls.conn.cursor()
        query = """SELECT COUNT(*) FROM users;"""
        with cls.conn:
            curr.execute(query)
            counter = curr.fetchone()[0]

        return counter
class Register(StatesGroup):
    firstname = State()
    lastname = State()
    email = State()

@dp.message(CommandStart())
async def start(message: Message, state: FSMContext):
    user = Database.search_user_by_chat_id(message.chat.id)
    if user is not None:
        await message.answer(f"Salom, {html.bold(user.first_name)}")
    else:
        await message.answer(f"Salom, {message.from_user.first_name} iltimos registratsiyadan o'tish uchun ismingizni kiriting!")
        await state.set_state(Register.firstname)

@dp.message(Register.firstname)
async def firstname(message: Message, state:FSMContext):
    if not message.text.isalpha():
        await message.answer(f"Ismda faqat harflar ishtirok etishi kerak")
        return

    ism = message.text.capitalize()
    await state.update_data(first_name=ism)
    await message.answer(f"Familyangizni kiriting")
    await state.set_state(Register.lastname)

@dp.message(Register.lastname)
async def lastname(message: Message, state:FSMContext):
    if not message.text.isalpha():
        await message.answer(f"Familiyada faqat harflar ishtirok etishi kerak")
        return

    familiya = message.text.capitalize()
    await state.update_data(last_name=familiya)
    await message.answer(f"Emailni kiriting")
    await state.set_state(Register.email)

@dp.message(Register.email)
async def email(message: Message, state:FSMContext):
    if not re.fullmatch(r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+", message.text):
        await message.answer(f"Iltimos Email kiriting")
        return

    email = message.text.lower()
    await state.update_data(email=email)
    user = await state.get_data()
    Database.add_user(**user, chat_id = message.chat.id)
    await state.clear()
    await message.answer(f"Registratsiya qilganingiz uchun raxmat, botdan foydalanishingiz mumkin😊")

@dp.message(Command("followers"))
async def followers(message: Message):
    foydalanuchilar_soni = Database.count_users()
    await message.answer(f"Foydalanuchilar soni {html.bold(foydalanuchilar_soni)} ta")

async def main() -> None:
    bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))

    await dp.start_polling(bot)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("EXIT")