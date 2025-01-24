from aiogram import types
from aiogram.filters import Command

from bot import dp


@dp.message(Command('start'))
async def welcome(message: types.Message):
    await message.answer(
        "*Добро пожаловать в бот поддержки Mytrade.kz!* \nВыберите интересующую вас категорию в разделе /menu",
        parse_mode="Markdown",
    )
