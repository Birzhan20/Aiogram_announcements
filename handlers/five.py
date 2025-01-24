from aiogram import types
from aiogram.enums import ParseMode

from bot import dp

from aiogram.utils.keyboard import InlineKeyboardBuilder


@dp.callback_query(lambda callback: callback.data == "question_4")
async def process_section_4(callback: types.CallbackQuery):
    questions_builder = InlineKeyboardBuilder()
    questions_builder.add(
        types.InlineKeyboardButton(
            text="Как найти нужный товар или услугу?",
            callback_data="16"))
    questions_builder.add(
        types.InlineKeyboardButton(
            text="Как связаться с продавцом?",
            callback_data="17"))
    questions_builder.add(
        types.InlineKeyboardButton(
            text="Можно ли вернуть товар?",
            callback_data="18"))
    questions_builder.add(
        types.InlineKeyboardButton(
            text="Как оплатить товар на платформе?",
            callback_data="19"))
    questions_builder.add(
        types.InlineKeyboardButton(
            text="Как получить гарантию на товар?",
            callback_data="20"))
    questions_builder.add(
        types.InlineKeyboardButton(
            text="Вернуться в главное меню",
            callback_data="main_menu"))
    questions_builder.adjust(1)

    await callback.answer("Вы выбрали раздел 'Покупки и продаж'", show_alert=True)
    await callback.message.edit_text(
        "*Выберите вопрос из раздела* _Покупки и продаж_:",
        reply_markup=questions_builder.as_markup(),
        parse_mode="Markdown"
    )
