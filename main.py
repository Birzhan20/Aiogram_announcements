import os
import asyncio
from aiogram import Bot, Dispatcher, types, F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.filters import Command
from aiogram.types import ContentType, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, desc, asc
from models import Listing, engine
from dotenv import load_dotenv
from states import CreateListing, DeleteListing, EditListing, ToggleListing, SearchListing

load_dotenv()

API_TOKEN = os.getenv('BOT_TOKEN')

bot = Bot(token=API_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(storage=storage)


@dp.message(Command('create'))  # создание записи в бд----------------------------------------------
async def start_create_listing(message: types.Message, state: FSMContext):
    await state.update_data(seller_username=message.from_user.username)
    await message.answer("Введите модель видеокарты:")
    await state.set_state(CreateListing.model)


@dp.message(CreateListing.model)
async def process_model(message: types.Message, state: FSMContext):
    await state.update_data(model=message.text)
    await message.answer("Укажите состояние (новая/б/у):")
    await state.set_state(CreateListing.condition)


@dp.message(CreateListing.condition)
async def process_condition(message: types.Message, state: FSMContext):
    await state.update_data(condition=message.text)
    await message.answer("Введите цену:")
    await state.set_state(CreateListing.price)


@dp.message(CreateListing.price)
async def process_price(message: types.Message, state: FSMContext):
    try:
        price = float(message.text)
        await state.update_data(price=price)
        await message.answer("Добавьте описание (до 500 символов):")
        await state.set_state(CreateListing.description)
    except ValueError:
        await message.answer("Пожалуйста, введите числовое значение для цены.")


@dp.message(CreateListing.description)
async def process_description(message: types.Message, state: FSMContext):
    await state.update_data(description=message.text)
    await message.answer("Загрузите до 3 фото товара.")
    await state.set_state(CreateListing.photos)


@dp.message(CreateListing.photos, F.content_type == ContentType.PHOTO)
async def process_photos(message: types.Message, state: FSMContext):
    data = await state.get_data()
    photos = data.get("photos", [])
    photos.append(message.photo[-1].file_id)
    await state.update_data(photos=photos)

    if len(photos) >= 3:
        await save_listing(state)
        await message.answer("Объявление успешно создано!")
        await state.clear()
    else:
        await message.answer("Загрузите еще фото или отправьте /done для завершения.")


@dp.message(Command("done"), CreateListing.photos)
async def done(message: types.Message, state: FSMContext):
    await save_listing(state)
    await message.answer("Объявление успешно создано!")
    await state.clear()


async def save_listing(state: FSMContext):
    data = await state.get_data()
    async with AsyncSession(engine) as session:
        new_listing = Listing(
            model=data["model"],
            condition=data["condition"],
            price=data["price"],
            description=data["description"],
            photo1=data["photos"][0] if len(data["photos"]) > 0 else None,
            photo2=data["photos"][1] if len(data["photos"]) > 1 else None,
            photo3=data["photos"][2] if len(data["photos"]) > 2 else None,
            seller_username=data["seller_username"]
        )
        try:
            session.add(new_listing)
            await session.commit()
        except Exception as e:
            await session.rollback()
            print(f"Ошибка при сохранении объявления: {e}")


# Редактирование
@dp.message(Command('all'))  # Все объявления выводит---------------------------------------------------
async def list_my_listings(message: types.Message):
    async with AsyncSession(engine) as session:
        listings = await session.execute(select(Listing))
        listings = listings.scalars().all()

    if listings:
        response = []
        for listing in listings:
            seller_username = listing.seller_username

            # Создаем кнопку для связи с продавцом
            button = InlineKeyboardButton(
                text="Связаться с продавцом",
                url=f"https://t.me/{seller_username}" if seller_username else "javascript:void(0)"
            )
            keyboard = InlineKeyboardMarkup(inline_keyboard=[[button]])

            response.append(f"{listing.id}: {listing.model} - {listing.price}₽")
            await message.answer(response[-1], reply_markup=keyboard)
    else:
        await message.answer("У вас нет объявлений.")


@dp.message(Command('edit'))  # Старт редактирования------------------------------------
async def edit_listing(message: types.Message, state: FSMContext):
    await message.answer("Введите ID объявления, которое хотите редактировать:")
    await state.set_state(EditListing.edit_listing_id)


@dp.message(EditListing.edit_listing_id)
async def process_edit_listing_id(message: types.Message, state: FSMContext):
    listing_id = int(message.text)
    async with AsyncSession(engine) as session:
        listing = await session.get(Listing, listing_id)

    if listing:
        await state.update_data(listing_id=listing_id)
        await message.answer("Введите новую цену:")
        await state.set_state(EditListing.edit_listing_price)
    else:
        await message.answer("Объявление не найдено. Попробуйте снова.")


@dp.message(EditListing.edit_listing_price)
async def process_edit_listing_price(message: types.Message, state: FSMContext):
    try:
        new_price = float(message.text)
        await state.update_data(new_price=new_price)
        await message.answer("Введите новое описание:")
        await state.set_state(EditListing.edit_listing_description)
    except ValueError:
        await message.answer("Пожалуйста, введите числовое значение для цены.")


@dp.message(EditListing.edit_listing_description)
async def process_edit_listing_description(message: types.Message, state: FSMContext):
    new_description = message.text
    data = await state.get_data()
    listing_id = data['listing_id']

    async with AsyncSession(engine) as session:
        listing = await session.get(Listing, listing_id)
        listing.price = data['new_price']
        listing.description = new_description
        await session.commit()

    await message.answer("Объявление успешно обновлено!")
    await state.clear()


# Удаление---------------------------------------------------------------
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


# Активировать или приостановить-----------------------------------------------------
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


# Команда для поиска------------------------------------------------------------
@dp.message(Command('search'))
async def search_listings(message: types.Message, state: FSMContext):
    await message.answer("Введите модель видеокарты для поиска:")
    await state.set_state(CreateListing.model)


@dp.message(CreateListing.model)
async def process_search_model(message: types.Message, state: FSMContext):
    await state.update_data(model=message.text)
    await message.answer("Введите минимальную цену (или оставьте пустым для пропуска):")
    await state.set_state(SearchListing.price_min)


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


async def main():
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
