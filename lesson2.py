import asyncio
import logging
import sys
# from curses.ascii import isdigit
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

load_dotenv()

TOKEN = getenv("BOT_TOKEN")

dp = Dispatcher(storage=MemoryStorage())


class GameState(StatesGroup):
    guessing = State()

@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    await message.answer(f"Hello, {html.bold(message.from_user.full_name)}!")

@dp.message(Command("oyin"))
async def game(msg: Message, state: FSMContext) -> None:
    gues_number = random.randint(1, 100)
    await state.set_state(GameState.guessing)
    await state.update_data(gues_number=gues_number, attempt=0)
    await msg.answer(f"Men son o`yladim uni toping")

@dp.message(GameState.guessing)
async def guess_handler(message: Message, state: FSMContext) -> None:
    state_data = await state.get_data()
    gues_number = state_data.get("gues_number")
    if not message.text.isdigit():
        await message.answer(f"1-100 oraligida son yozing")
        return
    elif not 1<=int(message.text)<=100:
        await message.answer(f"1-100 oraligida son yozing")
        return
    elif gues_number > int(message.text):
        attempt = state_data.get("attempt", 0) + 1
        await state.update_data(attempt=attempt)
        await message.answer(f"Men oylagan son kattaroq")
        return
    elif gues_number < int(message.text):
        attempt = state_data.get("attempt", 0) + 1
        await state.update_data(attempt=attempt)
        await message.answer(f"Men oylagan son kichikroq")
        return

    attempt = state_data.get("attempt", 0) + 1
    await state.update_data(attempt=attempt)
    await message.answer(f"Siz togri topdingiz, urinishlar soni: {attempt}")
    await state.clear()
    return
async def main() -> None:
    bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))

    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
