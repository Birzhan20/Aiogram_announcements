from aiogram import types
from bot import dp

from aiogram.utils.keyboard import InlineKeyboardBuilder


@dp.callback_query(lambda callback: callback.data == "5")
async def process_section_1(callback: types.CallbackQuery):
    questions_builder = InlineKeyboardBuilder()
    questions_builder.add(
        types.InlineKeyboardButton(
            text="Как создать интернет-магазин на Mytrade.kz?",
            callback_data="5.1"))
    questions_builder.add(
        types.InlineKeyboardButton(
            text="Какие преимущества у интернет-магазина?",
            callback_data="5.2"))
    questions_builder.add(
        types.InlineKeyboardButton(
            text="Как добавить товары в интернет-магазин?",
            callback_data="5.3"))
    questions_builder.add(
        types.InlineKeyboardButton(
            text="Как продвигать свой магазин?",
            callback_data="5.4"))
    questions_builder.add(
        types.InlineKeyboardButton(
            text="Как отслеживать статистику продаж?",
            callback_data="5.5"))
    questions_builder.adjust(1)

    await callback.message.answer(
        "Выберите вопрос из раздела 'О работе интернет-магазинов':",
        reply_markup=questions_builder.as_markup()
    )
