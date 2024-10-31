from aiogram import types
from aiogram.filters import Command

from bot import dp


@dp.message(Command('start'))
async def welcome(message: types.Message):
    await message.answer(
        "Добро пожаловать!\nЗдесь вы можете создавать свои объявления по продаже товаров.\nДля подробной информации введите команду /help"
    )
