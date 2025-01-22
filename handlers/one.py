from aiogram import types
from bot import dp

from aiogram.utils.keyboard import InlineKeyboardBuilder


@dp.callback_query(lambda callback: callback.data == "1")
async def process_section_1(callback: types.CallbackQuery):
    questions_builder = InlineKeyboardBuilder()
    questions_builder.add(
        types.InlineKeyboardButton(
            text="Как зарегистрироваться на Mytrade.kz?",
            callback_data="1.1"))
    questions_builder.add(
        types.InlineKeyboardButton(
            text="Как подтвердить свою учетную запись?",
            callback_data="1.2"))
    questions_builder.add(
        types.InlineKeyboardButton(
            text="Можно ли пользоваться платформой бесплатно?",
            callback_data="1.3"))
    questions_builder.add(
        types.InlineKeyboardButton(
            text="Какие услуги предоставляются для бизнеса?",
            callback_data="1.4"))
    questions_builder.add(
        types.InlineKeyboardButton(
            text="Как связаться с техподдержкой?",
            callback_data="1.5"))
    questions_builder.adjust(1)

    await callback.message.answer(
        "Выберите вопрос из раздела 'Общие':",
        reply_markup=questions_builder.as_markup()
    )
