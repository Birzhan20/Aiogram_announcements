from aiogram.fsm.context import FSMContext
from sqlalchemy.ext.asyncio import AsyncSession
from aiogram.filters import Command

from bot import dp
from models import Listing, engine
from states import ToggleListing
from aiogram import types


@dp.message(Command('status'))
async def toggle_listing(message: types.Message, state: FSMContext):
    await message.answer("Введите ID объявления, которое хотите активировать/приостановить:")
    await state.set_state(ToggleListing.toggle_listing_id)


@dp.message(ToggleListing.toggle_listing_id)
async def process_toggle_listing_id(message: types.Message, state: FSMContext):
    listing_id = int(message.text)
    async with AsyncSession(engine) as session:
        listing = await session.get(Listing, listing_id)

    if listing:
        listing.is_active = not listing.is_active
        await session.commit()
        status = "активировано" if listing.is_active else "приостановлено"
        await message.answer(f"Объявление успешно {status}.")
        await state.clear()
    else:
        await message.answer("Объявление не найдено.")
