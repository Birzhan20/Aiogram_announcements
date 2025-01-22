from aiogram import types
from bot import dp

from aiogram.utils.keyboard import InlineKeyboardBuilder


@dp.callback_query(lambda callback: callback.data == "4")
async def process_section_1(callback: types.CallbackQuery):
    questions_builder = InlineKeyboardBuilder()
    questions_builder.add(
        types.InlineKeyboardButton(
            text="Как найти нужный товар или услугу?",
            callback_data="4.1"))
    questions_builder.add(
        types.InlineKeyboardButton(
            text="Как связаться с продавцом?",
            callback_data="4.2"))
    questions_builder.add(
        types.InlineKeyboardButton(
            text="Можно ли вернуть товар?",
            callback_data="4.3"))
    questions_builder.add(
        types.InlineKeyboardButton(
            text="Как оплатить товар на платформе?",
            callback_data="4.4"))
    questions_builder.add(
        types.InlineKeyboardButton(
            text="Как получить гарантию на товар?",
            callback_data="4.5"))
    questions_builder.adjust(1)

    await callback.message.answer(
        "Выберите вопрос из раздела 'Покупки и продаж':",
        reply_markup=questions_builder.as_markup()
    )
