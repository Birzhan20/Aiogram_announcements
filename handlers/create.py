from aiogram import types, F
from aiogram.fsm.context import FSMContext
from aiogram.filters import Command
from aiogram.types import ContentType, ReplyKeyboardMarkup, KeyboardButton

from bot import dp
from states import CreateListing
from database import save_listing


@dp.message(Command('create'))
async def start_create_listing(message: types.Message, state: FSMContext):
    await state.update_data(seller_username=message.from_user.username)
    await message.answer("Введите модель видеокарты:")
    await state.set_state(CreateListing.model)


@dp.message(CreateListing.model)
async def process_model(message: types.Message, state: FSMContext):
    await state.update_data(model=message.text)
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Новое"), KeyboardButton(text="Б/у")]
        ],
        resize_keyboard=True
    )

    await message.answer("Укажите состояние:", reply_markup=keyboard)
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
