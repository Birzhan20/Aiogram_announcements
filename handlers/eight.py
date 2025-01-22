from aiogram import types
from bot import dp

from aiogram.utils.keyboard import InlineKeyboardBuilder


@dp.callback_query(lambda callback: callback.data == "8")
async def process_section_1(callback: types.CallbackQuery):
    questions_builder = InlineKeyboardBuilder()
    questions_builder.add(
        types.InlineKeyboardButton(
            text="Как оставить отзыв о продавце?",
            callback_data="8.1"))
    questions_builder.add(
        types.InlineKeyboardButton(
            text="Как повысить рейтинг моего магазина?",
            callback_data="8.2"))
    questions_builder.add(
        types.InlineKeyboardButton(
            text="Почему отзыв о товаре не был опубликован?",
            callback_data="8.3"))
    questions_builder.add(
        types.InlineKeyboardButton(
            text="Можно ли удалить негативный отзыв?",
            callback_data="8.4"))
    questions_builder.add(
        types.InlineKeyboardButton(
            text="Как пожаловаться на отзыв?",
            callback_data="8.5"))
    questions_builder.adjust(1)

    await callback.message.answer(
        "Выберите вопрос из раздела 'Рейтинги и отзывы':",
        reply_markup=questions_builder.as_markup()
    )
