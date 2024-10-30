from aiogram.fsm.context import FSMContext
from aiogram.types import KeyboardButton, ReplyKeyboardMarkup
from aiogram.filters import Command
from sqlalchemy import desc, asc, select
from sqlalchemy.ext.asyncio import AsyncSession

from bot import dp
from aiogram import types

from models import Listing, engine
from states import SearchListing


@dp.message(Command('search'))
async def search_listings(message: types.Message, state: FSMContext):
    await message.answer("Введите модель видеокарты для поиска:")
    await state.set_state(SearchListing.price_min)


@dp.message(SearchListing.price_min)
async def process_search_model(message: types.Message, state: FSMContext):
    await state.update_data(model=message.text)
    await message.answer("Введите минимальную цену (или оставьте пустым для пропуска):")
    await state.set_state(SearchListing.price_max)


@dp.message(SearchListing.price_max)
async def process_search_price_max(message: types.Message, state: FSMContext):
    max_price = message.text
    await state.update_data(price_max=max_price)

    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Дата"), KeyboardButton(text="Цена")]
        ],
        resize_keyboard=True
    )

    await message.answer("Выберите параметр сортировки:", reply_markup=keyboard)
    await state.set_state(SearchListing.sorting)


@dp.message(SearchListing.sorting)
async def process_sorting(message: types.Message, state: FSMContext):
    sorting_param = message.text.lower()
    data = await state.get_data()

    model = data.get("model")
    min_price = data.get("price_min")
    max_price = data.get("price_max")

    async with AsyncSession(engine) as session:
        query = select(Listing).where(Listing.model.ilike(f'%{model}%'))

        if min_price:
            query = query.where(Listing.price >= float(min_price))
        if max_price:
            query = query.where(Listing.price <= float(max_price))

        if sorting_param == 'дата':
            query = query.order_by(desc(Listing.date_added))
        elif sorting_param == 'цена':
            query = query.order_by(asc(Listing.price))

        listings = await session.execute(query)
        listings = listings.scalars().all()

    if listings:
        response = "\n".join(
            f"{listing.id}: {listing.model} - {listing.price}₽ ({'активно' if listing.is_active else 'приостановлено'})"
            for listing in listings)
        await message.answer(f"Найденные объявления:\n{response}")
    else:
        await message.answer("Объявления не найдены.")

    await state.clear()
