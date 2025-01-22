from aiogram import types
from bot import dp

from aiogram.utils.keyboard import InlineKeyboardBuilder


@dp.callback_query(lambda callback: callback.data == "2")
async def process_section_1(callback: types.CallbackQuery):
    questions_builder = InlineKeyboardBuilder()
    questions_builder.add(
        types.InlineKeyboardButton(
            text="Как разместить объявление?",
            callback_data="2.1"))
    questions_builder.add(
        types.InlineKeyboardButton(
            text="Как редактировать уже размещенное объявление?",
            callback_data="2.2"))
    questions_builder.add(
        types.InlineKeyboardButton(
            text="Как удалить объявление?",
            callback_data="2.3"))
    questions_builder.add(
        types.InlineKeyboardButton(
            text="Почему мое объявление не отображается?",
            callback_data="2.4"))
    questions_builder.add(
        types.InlineKeyboardButton(
            text="Как продвигать свое объявление?",
            callback_data="2.5"))
    questions_builder.adjust(1)

    await callback.message.answer(
        "Выберите вопрос из раздела 'Создание и управление объявлениями':",
        reply_markup=questions_builder.as_markup()
    )
