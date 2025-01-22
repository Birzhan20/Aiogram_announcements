from aiogram import types
from bot import dp

from aiogram.utils.keyboard import InlineKeyboardBuilder


@dp.callback_query(lambda callback: callback.data == "9")
async def process_section_1(callback: types.CallbackQuery):
    questions_builder = InlineKeyboardBuilder()
    questions_builder.add(
        types.InlineKeyboardButton(
            text="Почему сайт не открывается?",
            callback_data="9.1"))
    questions_builder.add(
        types.InlineKeyboardButton(
            text="Что делать, если не работает поиск?",
            callback_data="9.2"))
    questions_builder.add(
        types.InlineKeyboardButton(
            text="Почему изображения не загружаются?",
            callback_data="9.3"))
    questions_builder.add(
        types.InlineKeyboardButton(
            text="Как обновить контактные данные?",
            callback_data="9.4"))
    questions_builder.add(
        types.InlineKeyboardButton(
            text="Как отключить уведомления?",
            callback_data="9.5"))
    questions_builder.adjust(1)

    await callback.message.answer(
        "Выберите вопрос из раздела 'Технические вопросы':",
        reply_markup=questions_builder.as_markup()
    )
