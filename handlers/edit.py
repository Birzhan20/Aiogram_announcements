from aiogram import types, F
from aiogram.filters import Command
from aiogram.types import ContentType, ReplyKeyboardMarkup, KeyboardButton
from aiogram.fsm.context import FSMContext
from sqlalchemy.ext.asyncio import AsyncSession

from bot import dp
from database import save_changes
from models import Listing, engine
from states import EditListing


@dp.message(Command('edit'))
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
        await message.answer("Введите новое название (или отправьте /skip для пропуска):")
        await state.set_state(EditListing.edit_listing_name)
    else:
        await message.answer("Объявление не найдено. Попробуйте снова.")


@dp.message(EditListing.edit_listing_name)
async def process_edit_listing_name(message: types.Message, state: FSMContext):
    if message.text.strip() == "/skip":
        await state.update_data(new_name=None)
    else:
        await state.update_data(new_name=message.text.strip())

    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Новое"), KeyboardButton(text="Б/у")]
        ],
        resize_keyboard=True
    )

    await message.answer("Укажите состояние:", reply_markup=keyboard)
    await state.set_state(EditListing.edit_listing_condition)


@dp.message(EditListing.edit_listing_condition)
async def process_edit_listing_condition(message: types.Message, state: FSMContext):
    if message.text.strip() == "/skip":
        await state.update_data(new_condition=None)
    else:
        await state.update_data(new_condition=message.text.strip())

    await message.answer("Введите новую цену (или отправьте /skip для пропуска):")
    await state.set_state(EditListing.edit_listing_price)


@dp.message(EditListing.edit_listing_price)
async def process_edit_listing_price(message: types.Message, state: FSMContext):
    if message.text.strip() == "/skip":
        await state.update_data(new_price=None)
    else:
        try:
            new_price = float(message.text.strip())
            await state.update_data(new_price=new_price)
        except ValueError:
            await message.answer("Пожалуйста, введите корректное числовое значение или отправьте /skip для пропуска.")

    await message.answer("Введите новое описание (или отправьте /skip для пропуска):")
    await state.set_state(EditListing.edit_listing_description)


@dp.message(EditListing.edit_listing_description)
async def process_edit_listing_description(message: types.Message, state: FSMContext):
    if message.text.strip() == "/skip":
        await state.update_data(new_description=None)
    else:
        await state.update_data(new_description=message.text.strip())

    await message.answer("Загрузите новое фото (или отправьте /skip для пропуска):")
    await state.set_state(EditListing.edit_listing_photos)


@dp.message(EditListing.edit_listing_photos, F.content_type == ContentType.PHOTO)
async def process_edit_listing_photos(message: types.Message, state: FSMContext):
    data = await state.get_data()
    photos = data.get('photos', [])

    if message.photo:
        photos.append(message.photo[-1].file_id)
        await state.update_data(photos=photos)
        await message.answer(
            "Фото добавлено! Если хотите добавить ещё фото, загрузите его, или отправьте /done для завершения.")
    else:
        await message.answer("Не удалось получить фото, отправьте /done для завершения.")


@dp.message(Command('skip'), EditListing.edit_listing_photos)
@dp.message(Command('skip'), EditListing.edit_listing_description)
@dp.message(Command('skip'), EditListing.edit_listing_price)
@dp.message(Command('skip'), EditListing.edit_listing_condition)
@dp.message(Command('skip'), EditListing.edit_listing_name)
async def skip_field(message: types.Message, state: FSMContext):
    await message.answer("Поле пропущено.")
    await process_edit_listing_photos(message, state)


@dp.message(Command('done'), EditListing.edit_listing_photos)
async def done_editing(message: types.Message, state: FSMContext):
    await save_changes(state)
    await message.answer("Объявление успешно обновлено!")
    await state.clear()
