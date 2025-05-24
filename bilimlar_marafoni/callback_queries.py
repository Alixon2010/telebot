from aiogram.types import CallbackQuery
from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.utils.keyboard import InlineKeyboardMarkup, InlineKeyboardButton, InlineKeyboardBuilder, KeyboardButton, ReplyKeyboardMarkup
import random
from bilimlar_marafoni.game_classes.database.database import Database
from bilimlar_marafoni.main import Play

call_router = Router()

quizes = Database.load_questions()
def choose_subcategory():
    keyboard = [[
        InlineKeyboardButton(text="1-sinf", callback_data="1-sinf"),
        InlineKeyboardButton(text="2-sinf", callback_data="2-sinf"),
        InlineKeyboardButton(text="3-sinf", callback_data="3-sinf")],
        [InlineKeyboardButton(text="4-sinf", callback_data="4-sinf"),
         InlineKeyboardButton(text="5-sinf", callback_data="5-sinf"),
         InlineKeyboardButton(text="6-sinf", callback_data="6-sinf")],
        [InlineKeyboardButton(text="7-sinf", callback_data="7-sinf"),
         InlineKeyboardButton(text="8-sinf", callback_data="8-sinf"),
         InlineKeyboardButton(text="9-sinf", callback_data="9-sinf")],
        [InlineKeyboardButton(text="10-sinf", callback_data="10-sinf"),
         InlineKeyboardButton(text="11-sinf", callback_data="11-sinf")],
        [InlineKeyboardButton(text="Orqaga", callback_data="orqaga")]
    ]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)

def choose_category():
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(text="📊 Matematika", callback_data="matematika"),
        InlineKeyboardButton(text="⚛️ Fizika", callback_data="fizika"),
        InlineKeyboardButton(text="🎓 Ingliz tili", callback_data="english"),
    )
    builder.adjust(2,1)
    return builder.as_markup()

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


@call_router.callback_query(F.data=="orqaga")
async def callback_query(call: CallbackQuery):
    await call.answer()
    await call.message.edit_text(f"Kategorya tanlang", reply_markup=choose_category())

@call_router.callback_query(F.data.in_({'matematika', 'fizika', 'english'}))
async def callback_query(call: CallbackQuery, state: FSMContext):
    await call.answer()
    await state.update_data(category=call.data)
    await call.message.edit_text("📘Sinfni tanlang", reply_markup=choose_subcategory())

@call_router.callback_query(F.data.in_({'1-sinf', '2-sinf', '3-sinf', '4-sinf', '5-sinf', '6-sinf', '7-sinf', '8-sinf', '9-sinf', '10-sinf', '11-sinf'}))
async def callback_query(call: CallbackQuery, state: FSMContext):
    await call.answer()
    data = await state.get_data()
    category = data['category']
    subcategory = call.data
    savollar = random.sample(Database.load_questions_by_category_and_subcategory(category, subcategory, quizes), 5)
    await call.message.delete()
    await call.message.answer(str(savollar[0]), reply_markup=variant_btn(savollar[0].get_variants()))
    await state.update_data(chat_id=call.message.chat.id, ball=0, savollar=savollar, savol_index=0)
    await state.set_state(Play.play)
