from aiogram import types
from aiogram.enums import ParseMode

from bot import dp

from aiogram.utils.keyboard import InlineKeyboardBuilder


@dp.callback_query(lambda callback: callback.data == "question_8")
async def process_section_1(callback: types.CallbackQuery):
    questions_builder = InlineKeyboardBuilder()
    questions_builder.add(
        types.InlineKeyboardButton(
            text="Как оставить отзыв о продавце?",
            callback_data="36"))
    questions_builder.add(
        types.InlineKeyboardButton(
            text="Как повысить рейтинг моего магазина?",
            callback_data="37"))
    questions_builder.add(
        types.InlineKeyboardButton(
            text="Почему отзыв о товаре не был опубликован?",
            callback_data="38"))
    questions_builder.add(
        types.InlineKeyboardButton(
            text="Можно ли удалить негативный отзыв?",
            callback_data="39"))
    questions_builder.add(
        types.InlineKeyboardButton(
            text="Как пожаловаться на отзыв?",
            callback_data="40"))
    questions_builder.add(
        types.InlineKeyboardButton(
            text="Вернуться в главное меню",
            callback_data="main_menu"))
    questions_builder.adjust(1)

    await callback.answer("Вы выбрали раздел 'Рейтинги и отзывы'", show_alert=True)
    await callback.message.edit_text(
        "Выберите вопрос из раздела <b><i>Рейтинги и отзывы</i></b>:",
        reply_markup=questions_builder.as_markup(),
        parse_mode=ParseMode.HTML
    )
