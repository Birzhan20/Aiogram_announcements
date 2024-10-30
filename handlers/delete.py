from aiogram.fsm.context import FSMContext
from sqlalchemy.ext.asyncio import AsyncSession
from aiogram.filters import Command

from bot import dp
from models import Listing, engine
from states import DeleteListing
from aiogram import types


@dp.message(Command('delete'))
async def delete_listing(message: types.Message, state: FSMContext):
    await message.answer("Введите ID объявления, которое хотите удалить:")
    await state.set_state(DeleteListing.delete_listing_id)


@dp.message(DeleteListing.delete_listing_id)
async def process_delete_listing_id(message: types.Message):
    try:
        listing_id = int(message.text)
        async with AsyncSession(engine) as session:
            listing = await session.get(Listing, listing_id)

        if listing:
            async with session.begin():
                await session.delete(listing)
            await message.answer("Объявление успешно удалено!")
        else:
            await message.answer("Объявление не найдено.")
    except ValueError:
        await message.answer("Пожалуйста, введите корректный ID объявления.")
