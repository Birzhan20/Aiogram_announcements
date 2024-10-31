from aiogram.fsm.context import FSMContext
from aiogram.types import KeyboardButton, ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup, \
    InputMediaPhoto
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
    await state.set_state(SearchListing.model)


@dp.message(SearchListing.model)
async def process_search_model(message: types.Message, state: FSMContext):
    await state.update_data(model=message.text)
    await message.answer("Введите минимальную цену:")
    await state.set_state(SearchListing.price_min)


@dp.message(SearchListing.price_min)
async def process_search_price_min(message: types.Message, state: FSMContext):
    try:
        min_price = int(message.text)
    except ValueError:
        await message.answer("Пожалуйста, введите корректное числовое значение для минимальной цены.")
        return
    await state.update_data(price_min=min_price)
    await message.answer("Введите максимальную цену:")
    await state.set_state(SearchListing.price_max)


@dp.message(SearchListing.price_max)
async def process_search_price_max(message: types.Message, state: FSMContext):
    try:
        max_price = int(message.text)
    except ValueError:
        await message.answer("Пожалуйста, введите корректное числовое значение для максимальной цены.")
        return
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
        for listing in listings:
            seller_username = listing.seller_username

            button = InlineKeyboardButton(
                text="Связаться с продавцом",
                url=f"https://t.me/{seller_username}" if seller_username else "javascript:void(0)"
            )
            keyboard = InlineKeyboardMarkup(inline_keyboard=[[button]])

            response = (
                f"ID: {listing.id}\n"
                f"Модель: {listing.model}\n"
                f"Цена: {listing.price}\n"
                f"Состояние: {listing.condition}\n"
                f"Описание: {listing.description}\n"
                f"Статус: {'Активно' if listing.is_active else 'Приостановлено'}\n"
            )

            media_group = []
            if listing.photo1:
                media_group.append(InputMediaPhoto(media=listing.photo1))
            if listing.photo2:
                media_group.append(InputMediaPhoto(media=listing.photo2))
            if listing.photo3:
                media_group.append(InputMediaPhoto(media=listing.photo3))

            if media_group:
                await message.answer_media_group(media=media_group)
                await message.answer(response, reply_markup=keyboard)
            else:
                await message.answer(response, reply_markup=keyboard)
    else:
        await message.answer("Объявления не найдены.")

    await state.clear()
