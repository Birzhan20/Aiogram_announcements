from aiogram import types
from bot import dp

from aiogram.utils.keyboard import InlineKeyboardBuilder


@dp.callback_query(lambda callback: callback.data == "10")
async def process_section_1(callback: types.CallbackQuery):
    questions_builder = InlineKeyboardBuilder()
    questions_builder.add(
        types.InlineKeyboardButton(
            text="Какие правила размещения объявлений?",
            callback_data="10.1"))
    questions_builder.add(
        types.InlineKeyboardButton(
            text="Можно ли разместить одно объявление в нескольких категориях?",
            callback_data="10.2"))
    questions_builder.add(
        types.InlineKeyboardButton(
            text="Как изменить язык интерфейса?",
            callback_data="10.3"))
    questions_builder.add(
        types.InlineKeyboardButton(
            text="Можно ли использовать платформу из другой страны?",
            callback_data="10.4"))
    questions_builder.add(
        types.InlineKeyboardButton(
            text="Какие условия для сотрудничества с Mytrade.kz?",
            callback_data="10.5"))
    questions_builder.adjust(1)

    await callback.message.answer(
        "Выберите вопрос из раздела 'Прочие вопросы':",
        reply_markup=questions_builder.as_markup()
    )
