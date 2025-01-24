from aiogram import types
from aiogram.enums import ParseMode
from aiogram.utils.keyboard import InlineKeyboardBuilder

from bot import dp
from core.config import AsyncSessionLocal
from core.database import get_answer_by_id
from models import Listing

from sqlalchemy.future import select


@dp.callback_query(lambda callback: callback.data == "question_1")
async def process_section_1(callback: types.CallbackQuery):
    questions_builder = InlineKeyboardBuilder()
    questions_builder.add(
        types.InlineKeyboardButton(
            text="Как зарегистрироваться на Mytrade.kz?",
            callback_data="1"))
    questions_builder.add(
        types.InlineKeyboardButton(
            text="Как подтвердить свою учетную запись?",
            callback_data="2"))
    questions_builder.add(
        types.InlineKeyboardButton(
            text="Можно ли пользоваться платформой бесплатно?",
            callback_data="3"))
    questions_builder.add(
        types.InlineKeyboardButton(
            text="Какие услуги предоставляются для бизнеса?",
            callback_data="4"))
    questions_builder.add(
        types.InlineKeyboardButton(
            text="Как связаться с техподдержкой?",
            callback_data="5"))
    questions_builder.add(
        types.InlineKeyboardButton(
            text="Вернуться в главное меню",
            callback_data="main_menu"))
    questions_builder.adjust(1)

    await callback.answer("Вы выбрали раздел 'Общие'", show_alert=True)
    await callback.message.edit_text(
        "Выберите вопрос из раздела <b><i>Общие</i></b>:",
        reply_markup=questions_builder.as_markup(),
        parse_mode=ParseMode.HTML
    )
