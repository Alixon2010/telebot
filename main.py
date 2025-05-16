import asyncio
import logging
import sys
from os import getenv

from aiogram import Bot, Dispatcher, html, F
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import Message
from dotenv import load_dotenv

from datetime import datetime

load_dotenv()
TOKEN = getenv("BOT_TOKEN")

ADMIN = getenv("ADMIN")
ARDIG = getenv("ARDIG")
dp = Dispatcher()


def __eq__(self, other):
    return lambda sfgr: self.value == other.value


@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    await message.answer(f"<a href=\"https://youtu.be/nENUBulDXKA?si=XKKH-92AyH4wPjOP\">bos</a>")


@dp.message(F.text.regexp(r'^\d{2}-\d{2}-\d{4}$'))
async def year_to_age(message: Message):
    a = datetime.strptime(datetime.now().strftime("%m-%d-%Y"), "%m-%d-%Y")

    c = datetime.strptime(message.text, "%d-%m-%Y")

    res = a - c
    result = res.days / 365
    await message.answer(f"Тебе {str(int(result))} лет")


@dp.message(F.text.regexp(r'^(100|[1-9]?[0-9])$'))
async def age_to_year(message: Message):
    await message.answer(str(2025 - int(message.text)))


# @dp.message(F.text == "/oyin")
# async def oyin(message: Message) -> None:
#     number = randint(1, 100)
#     await message.answer("Son o'ylandi")

@dp.message(lambda message: message.text.split()[0] == '/ardig')
async def message_to_ardig(message: Message) -> None:
    global ARDIG
    await message.send_copy(chat_id=ARDIG)


@dp.message()
async def echo_handler(message: Message) -> None:
    try:
        await message.send_copy(chat_id=message.chat.id)
    except TypeError:
        await message.answer("Yana urinib kor!")


async def main() -> None:
    bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))

    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
    print("Done")
