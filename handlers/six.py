from aiogram import types
from aiogram.enums import ParseMode

from bot import dp

from aiogram.utils.keyboard import InlineKeyboardBuilder


@dp.callback_query(lambda callback: callback.data == "question_6")
async def process_section_1(callback: types.CallbackQuery):
    questions_builder = InlineKeyboardBuilder()
    questions_builder.add(
        types.InlineKeyboardButton(
            text="Как организовать доставку товаров?",
            callback_data="26"))
    questions_builder.add(
        types.InlineKeyboardButton(
            text="Какие способы оплаты поддерживаются?",
            callback_data="27"))
    questions_builder.add(
        types.InlineKeyboardButton(
            text="Можно ли оплатить через Kaspi.kz?",
            callback_data="28"))
    questions_builder.add(
        types.InlineKeyboardButton(
            text="Как изменить адрес доставки?",
            callback_data="29"))
    questions_builder.add(
        types.InlineKeyboardButton(
            text="Что делать, если товар не был доставлен?",
            callback_data="30"))
    questions_builder.add(
        types.InlineKeyboardButton(
            text="Вернуться в главное меню",
            callback_data="main_menu"))
    questions_builder.adjust(1)

    await callback.answer("Вы выбрали раздел 'Доставка и оплата'", show_alert=True)
    await callback.message.edit_text(
        "Выберите вопрос из раздела <b><i>Доставка и оплата</i></b>:",
        reply_markup=questions_builder.as_markup(),
        parse_mode=ParseMode.HTML
    )
