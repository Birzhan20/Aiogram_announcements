from aiogram import types
from bot import dp

from aiogram.utils.keyboard import InlineKeyboardBuilder


@dp.callback_query(lambda callback: callback.data == "7")
async def process_section_1(callback: types.CallbackQuery):
    questions_builder = InlineKeyboardBuilder()
    questions_builder.add(
        types.InlineKeyboardButton(
            text="Какие рекламные услуги предоставляет Mytrade.kz??",
            callback_data="7.1"))
    questions_builder.add(
        types.InlineKeyboardButton(
            text="Как настроить рекламу для объявлений?",
            callback_data="7.2"))
    questions_builder.add(
        types.InlineKeyboardButton(
            text="Как продвигать товары через социальные сети?",
            callback_data="7.3"))
    questions_builder.add(
        types.InlineKeyboardButton(
            text="Как узнать, какая реклама работает лучше всего?",
            callback_data="7.4"))
    questions_builder.add(
        types.InlineKeyboardButton(
            text="Какие есть скидки на рекламные пакеты?",
            callback_data="7.5"))
    questions_builder.adjust(1)

    await callback.message.answer(
        "Выберите вопрос из раздела 'Продвижение и реклама':",
        reply_markup=questions_builder.as_markup()
    )
