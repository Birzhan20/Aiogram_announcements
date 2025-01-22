from aiogram import types
from aiogram.filters import Command
from aiogram.utils.keyboard import InlineKeyboardBuilder

from bot import dp


@dp.message(Command("help"))
async def cmd_random(message: types.Message):
    builder = InlineKeyboardBuilder()
    builder.add(types.InlineKeyboardButton(text="Общие", callback_data="1"))
    builder.add(
        types.InlineKeyboardButton(
            text="Создание и управление объявлениями",
            callback_data="2"))
    builder.add(
        types.InlineKeyboardButton(
            text="Безопасность",
            callback_data="3"))
    builder.add(
        types.InlineKeyboardButton(
            text="Покупки и продажи",
            callback_data="4"))
    builder.add(
        types.InlineKeyboardButton(
            text="О работе интернет-магазинов",
            callback_data="5"))
    builder.add(
        types.InlineKeyboardButton(
            text="Доставка и оплата",
            callback_data="6"))
    builder.add(
        types.InlineKeyboardButton(
            text="Продвижение и реклама",
            callback_data="7"))
    builder.add(
        types.InlineKeyboardButton(
            text="Рейтинги и отзывы",
            callback_data="8"))
    builder.add(
        types.InlineKeyboardButton(
            text="Технические вопросы",
            callback_data="9"))
    builder.add(
        types.InlineKeyboardButton(
            text="Прочие вопросы",
            callback_data="10"))
    builder.adjust(1)
    await message.answer(
        "Выберите раздел по вашему вопросу:",
        reply_markup=builder.as_markup()
    )
