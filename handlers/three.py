from aiogram import types
from bot import dp

from aiogram.utils.keyboard import InlineKeyboardBuilder


@dp.callback_query(lambda callback: callback.data == "3")
async def process_section_1(callback: types.CallbackQuery):
    questions_builder = InlineKeyboardBuilder()
    questions_builder.add(
        types.InlineKeyboardButton(
            text="Как защитить свою учетную запись?",
            callback_data="3.1"))
    questions_builder.add(
        types.InlineKeyboardButton(
            text="Что делать, если забыл пароль?",
            callback_data="3.2"))
    questions_builder.add(
        types.InlineKeyboardButton(
            text="Как восстановить доступ к учетной записи?",
            callback_data="3.3"))
    questions_builder.add(
        types.InlineKeyboardButton(
            text="Как пожаловаться на мошенничество?",
            callback_data="3.4"))
    questions_builder.add(
        types.InlineKeyboardButton(
            text="Как избежать мошенников на платформе?",
            callback_data="3.5"))
    questions_builder.adjust(1)

    await callback.message.answer(
        "Выберите вопрос из раздела 'Безопасность':",
        reply_markup=questions_builder.as_markup()
    )
