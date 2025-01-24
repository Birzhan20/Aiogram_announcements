from aiogram import types
from aiogram.enums import ParseMode

from bot import dp

from aiogram.utils.keyboard import InlineKeyboardBuilder


@dp.callback_query(lambda callback: callback.data == "question_2")
async def process_section_2(callback: types.CallbackQuery):
    questions_builder = InlineKeyboardBuilder()
    questions_builder.add(
        types.InlineKeyboardButton(
            text="Как разместить объявление?",
            callback_data="6"))
    questions_builder.add(
        types.InlineKeyboardButton(
            text="Как редактировать уже размещенное объявление?",
            callback_data="7"))
    questions_builder.add(
        types.InlineKeyboardButton(
            text="Как удалить объявление?",
            callback_data="8"))
    questions_builder.add(
        types.InlineKeyboardButton(
            text="Почему мое объявление не отображается?",
            callback_data="9"))
    questions_builder.add(
        types.InlineKeyboardButton(
            text="Как продвигать свое объявление?",
            callback_data="10"))
    questions_builder.add(
        types.InlineKeyboardButton(
            text="Вернуться в главное меню",
            callback_data="main_menu"))
    questions_builder.adjust(1)

    await callback.answer("Вы выбрали раздел 'Создание и управление объявлениями'", show_alert=True)
    await callback.message.edit_text(
        "*Выберите вопрос из раздела* _Создание и управление объявлениями_:",
        reply_markup=questions_builder.as_markup(),
        parse_mode="Markdown"
    )
