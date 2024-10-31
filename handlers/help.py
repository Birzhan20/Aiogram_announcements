from aiogram import types
from aiogram.filters import Command

from bot import dp


@dp.message(Command('help'))
async def intro(message: types.Message):
    await message.answer(
        "Команды:\n/create - создать объявление\n/edit - редактировать объявление\n/search - искать товар по фильтрам\n/status - менять статус объявления\n/delete - удаление\n/all - список всех объявлений"
    )
