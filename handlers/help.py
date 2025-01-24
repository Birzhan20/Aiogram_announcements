from aiogram import types
from aiogram.enums import ParseMode
from aiogram.filters import Command
from aiogram.utils.keyboard import InlineKeyboardBuilder

from bot import dp, bot


@dp.message(Command("menu"))
async def cmd_random(message: types.Message):
    builder = InlineKeyboardBuilder()
    builder.add(types.InlineKeyboardButton(text="Общие", callback_data="question_1"))
    builder.add(
        types.InlineKeyboardButton(
            text="Создание и управление объявлениями",
            callback_data="question_2"))
    builder.add(
        types.InlineKeyboardButton(
            text="Безопасность",
            callback_data="question_3"))
    builder.add(
        types.InlineKeyboardButton(
            text="Покупки и продажи",
            callback_data="question_4"))
    builder.add(
        types.InlineKeyboardButton(
            text="О работе интернет-магазинов",
            callback_data="question_5"))
    builder.add(
        types.InlineKeyboardButton(
            text="Доставка и оплата",
            callback_data="question_6"))
    builder.add(
        types.InlineKeyboardButton(
            text="Продвижение и реклама",
            callback_data="question_7"))
    builder.add(
        types.InlineKeyboardButton(
            text="Рейтинги и отзывы",
            callback_data="question_8"))
    builder.add(
        types.InlineKeyboardButton(
            text="Технические вопросы",
            callback_data="question_9"))
    builder.add(
        types.InlineKeyboardButton(
            text="Прочие вопросы",
            callback_data="question_10"))
    builder.adjust(1)
    await message.answer(
        "*Выберите раздел по вашему вопросу:*",
        reply_markup=builder.as_markup(),
        parse_mode="Markdown"
    )


@dp.callback_query(lambda callback: callback.data == "main_menu")
async def handle_main_menu(callback_query: types.CallbackQuery):
    await bot.send_message(callback_query.from_user.id, "Вы вернулись в главное меню.")
    await cmd_random(callback_query.message)
