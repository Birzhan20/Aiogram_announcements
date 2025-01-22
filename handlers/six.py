from aiogram import types
from bot import dp

from aiogram.utils.keyboard import InlineKeyboardBuilder


@dp.callback_query(lambda callback: callback.data == "6")
async def process_section_1(callback: types.CallbackQuery):
    questions_builder = InlineKeyboardBuilder()
    questions_builder.add(
        types.InlineKeyboardButton(
            text="Как организовать доставку товаров?",
            callback_data="6.1"))
    questions_builder.add(
        types.InlineKeyboardButton(
            text="Какие способы оплаты поддерживаются?",
            callback_data="6.2"))
    questions_builder.add(
        types.InlineKeyboardButton(
            text="Можно ли оплатить через Kaspi.kz?",
            callback_data="6.3"))
    questions_builder.add(
        types.InlineKeyboardButton(
            text="Как изменить адрес доставки?",
            callback_data="6.4"))
    questions_builder.add(
        types.InlineKeyboardButton(
            text="Что делать, если товар не был доставлен?",
            callback_data="6.5"))
    questions_builder.adjust(1)

    await callback.message.answer(
        "Выберите вопрос из раздела 'Доставка и оплата':",
        reply_markup=questions_builder.as_markup()
    )
