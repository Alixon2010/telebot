from aiogram.enums import ParseMode

from bilimlar_marafoni.game_classes.database.database import Database

from aiogram.utils.keyboard import InlineKeyboardBuilder

from datetime import datetime

import asyncio
import logging
import sys
import random

from collections import defaultdict

from os import getenv
from dotenv import load_dotenv
from aiogram.types import Message, ReplyKeyboardRemove, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, \
    InlineKeyboardMarkup
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.fsm.context import FSMContext
from aiogram import Bot, Dispatcher, html, F
from aiogram.fsm.state import State, StatesGroup
from aiogram.client.default import DefaultBotProperties
from aiogram.filters import CommandStart, Command

load_dotenv()
dp = Dispatcher(storage=MemoryStorage())


def variant_btn(variants):
    buttons = [
        [
            KeyboardButton(text=variants[0]),
            KeyboardButton(text=variants[1]),
        ],
        [
            KeyboardButton(text=variants[2]),
            KeyboardButton(text=variants[3]),
        ]
    ]
    markup = ReplyKeyboardMarkup(keyboard=buttons, resize_keyboard=True)

    return markup


class Play(StatesGroup):
    start = State()
    play = State()


@dp.message(CommandStart())
async def start(message: Message):
    await message.answer(f"Salom, {html.bold(message.from_user.first_name)}\n\n"
                         f"O'yinni boshlash uchun /play ni bosing")


@dp.message(Command("play"))
async def play(message: Message, state: FSMContext):
    buttons = [[
        KeyboardButton(text="Ha"),
        KeyboardButton(text="Yo'q")
    ]]
    markup = ReplyKeyboardMarkup(keyboard=buttons, resize_keyboard=True)
    await message.answer(f"O'yinni boshlaysizmi?", reply_markup=markup)
    await state.set_state(Play.start)


def choose_category():
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(text="📊 Matematika", callback_data="matematika"),
        InlineKeyboardButton(text="⚛️ Fizika", callback_data="fizika"),
        InlineKeyboardButton(text="🎓 Ingliz tili", callback_data="english"),
    )
    builder.adjust(2,1)
    return builder.as_markup()


@dp.message(Play.start)
async def start(message: Message, state: FSMContext):
    if message.text.lower() == "ha":
        if Database.search_user_by_chat_id(message.chat.id) is None:
            Database.save_user(int(message.chat.id), message.from_user.first_name)
        await message.answer(f"🗃️Kategorya tanlang", reply_markup=choose_category())


@dp.message(Play.play)
async def game(message: Message, state: FSMContext):
    data = await state.get_data()
    index = data["savol_index"]
    savol = data["savollar"][index]
    ball = data["ball"]

    if savol.check_answer(message.text):
        ball += 10
        await state.update_data(ball=ball)
        await message.answer("Bu to'g'ri javob sizga 10 ball qo'shildi🥳🎉")
        Database.save_results(message.chat.id, savol.id, savol.get_option_id(message.text),
                              datetime.now().strftime("%d/%m/%Y %H:%M:%S"))
    else:
        await message.answer("Bu javob xato☹️")
        Database.save_results(message.chat.id, savol.id, savol.get_option_id(message.text),
                              datetime.now().strftime("%d/%m/%Y %H:%M:%S"))

    try:
        keyingi_savol = data["savollar"][index + 1]
        keyingi_variantlar = keyingi_savol.get_variants()
    except IndexError:
        await message.answer("Savollar tugadi😮‍💨", reply_markup=ReplyKeyboardRemove())
    else:
        await state.update_data(savol=keyingi_savol, savol_index=index + 1)
        await message.answer(str(keyingi_savol), reply_markup=variant_btn(keyingi_variantlar))


async def main():
    from bilimlar_marafoni.callback_queries import call_router

    bot = Bot(token=getenv("BOT_TOKEN"), default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    dp.include_routers(call_router)
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("EXIT...")