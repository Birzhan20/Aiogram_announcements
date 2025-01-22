from aiogram import types
from aiogram.filters import Filter
from aiogram.fsm.context import FSMContext
from bot import dp

@dp.callback_query(lambda callback: callback.data == "8")
async def send_random_value(callback: types.CallbackQuery):
    await callback.message.answer("saske")