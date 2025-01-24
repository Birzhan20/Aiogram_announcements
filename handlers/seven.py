from aiogram import types
from aiogram.enums import ParseMode

from bot import dp

from aiogram.utils.keyboard import InlineKeyboardBuilder


@dp.callback_query(lambda callback: callback.data == "question_7")
async def process_section_1(callback: types.CallbackQuery):
    questions_builder = InlineKeyboardBuilder()
    questions_builder.add(
        types.InlineKeyboardButton(
            text="Какие рекламные услуги предоставляет Mytrade.kz??",
            callback_data="31"))
    questions_builder.add(
        types.InlineKeyboardButton(
            text="Как настроить рекламу для объявлений?",
            callback_data="32"))
    questions_builder.add(
        types.InlineKeyboardButton(
            text="Как продвигать товары через социальные сети?",
            callback_data="33"))
    questions_builder.add(
        types.InlineKeyboardButton(
            text="Как работает реклама историй и логотипов?",
            callback_data="34"))
    questions_builder.add(
        types.InlineKeyboardButton(
            text="Какие есть скидки на рекламные пакеты?",
            callback_data="35"))
    questions_builder.add(
        types.InlineKeyboardButton(
            text="Вернуться в главное меню",
            callback_data="main_menu"))
    questions_builder.adjust(1)

    await callback.answer("Вы выбрали раздел 'Продвижение и реклама'", show_alert=True)
    await callback.message.edit_text(
        "Выберите вопрос из раздела <b><i>Продвижение и реклама</i></b>:",
        reply_markup=questions_builder.as_markup(),
        parse_mode=ParseMode.HTML
    )
