from aiogram import types
from aiogram.enums import ParseMode

from bot import dp

from aiogram.utils.keyboard import InlineKeyboardBuilder


@dp.callback_query(lambda callback: callback.data == "question_3")
async def process_section_3(callback: types.CallbackQuery):
    questions_builder = InlineKeyboardBuilder()
    questions_builder.add(
        types.InlineKeyboardButton(
            text="Как защитить свою учетную запись?",
            callback_data="11"))
    questions_builder.add(
        types.InlineKeyboardButton(
            text="Что делать, если забыл пароль?",
            callback_data="12"))
    questions_builder.add(
        types.InlineKeyboardButton(
            text="Как восстановить доступ к учетной записи?",
            callback_data="13"))
    questions_builder.add(
        types.InlineKeyboardButton(
            text="Как пожаловаться на мошенничество?",
            callback_data="14"))
    questions_builder.add(
        types.InlineKeyboardButton(
            text="Как избежать мошенников на платформе?",
            callback_data="15"))
    questions_builder.add(
        types.InlineKeyboardButton(
            text="Вернуться в главное меню",
            callback_data="main_menu"))
    questions_builder.adjust(1)

    await callback.answer("Вы выбрали раздел 'Безопасность'", show_alert=True)
    await callback.message.edit_text(
        "*Выберите вопрос из раздела* _Безопасность_:",
        reply_markup=questions_builder.as_markup(),
        parse_mode="Markdown"
    )
