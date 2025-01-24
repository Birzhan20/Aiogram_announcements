from aiogram import types
from aiogram.enums import ParseMode

from bot import dp

from aiogram.utils.keyboard import InlineKeyboardBuilder


@dp.callback_query(lambda callback: callback.data == "question_10")
async def process_section_1(callback: types.CallbackQuery):
    questions_builder = InlineKeyboardBuilder()
    questions_builder.add(
        types.InlineKeyboardButton(
            text="Какие правила размещения объявлений?",
            callback_data="46"))
    questions_builder.add(
        types.InlineKeyboardButton(
            text="Можно ли разместить одно объявление в нескольких категориях?",
            callback_data="47"))
    questions_builder.add(
        types.InlineKeyboardButton(
            text="Как изменить язык интерфейса?",
            callback_data="48"))
    questions_builder.add(
        types.InlineKeyboardButton(
            text="На каких языках доступен контент Mytrade.kz?",
            callback_data="49"))
    questions_builder.add(
        types.InlineKeyboardButton(
            text="На каких языках можно публиковать объявления на Mytrade.kz?",
            callback_data="50"))
    questions_builder.add(
        types.InlineKeyboardButton(
            text="Можно ли использовать платформу из другой страны?",
            callback_data="51"))
    questions_builder.add(
        types.InlineKeyboardButton(
            text="Какие условия для сотрудничества с Mytrade.kz?",
            callback_data="52"))
    questions_builder.add(
        types.InlineKeyboardButton(
            text="Вернуться в главное меню",
            callback_data="main_menu"))
    questions_builder.adjust(1)

    await callback.answer("Вы выбрали раздел 'Прочие вопросы'", show_alert=True)
    await callback.message.edit_text(
        "Выберите вопрос из раздела <b><i>Прочие вопросы</i></b>:",
        reply_markup=questions_builder.as_markup(),
        parse_mode=ParseMode.HTML
    )
