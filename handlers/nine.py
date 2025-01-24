from aiogram import types
from aiogram.enums import ParseMode

from bot import dp

from aiogram.utils.keyboard import InlineKeyboardBuilder


@dp.callback_query(lambda callback: callback.data == "question_9")
async def process_section_1(callback: types.CallbackQuery):
    questions_builder = InlineKeyboardBuilder()
    questions_builder.add(
        types.InlineKeyboardButton(
            text="Почему сайт не открывается?",
            callback_data="41"))
    questions_builder.add(
        types.InlineKeyboardButton(
            text="Что делать, если не работает поиск?",
            callback_data="42"))
    questions_builder.add(
        types.InlineKeyboardButton(
            text="Почему изображения не загружаются?",
            callback_data="43"))
    questions_builder.add(
        types.InlineKeyboardButton(
            text="Как обновить контактные данные?",
            callback_data="44"))
    questions_builder.add(
        types.InlineKeyboardButton(
            text="Как отключить уведомления?",
            callback_data="45"))
    questions_builder.add(
        types.InlineKeyboardButton(
            text="Вернуться в главное меню",
            callback_data="main_menu"))
    questions_builder.adjust(1)

    await callback.answer("Вы выбрали раздел 'Технические вопросы'", show_alert=True)
    await callback.message.edit_text(
        "Выберите вопрос из раздела <b><i>Технические вопросы</i></b>:",
        reply_markup=questions_builder.as_markup(),
        parse_mode=ParseMode.HTML
    )
