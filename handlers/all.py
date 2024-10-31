from aiogram import types
from aiogram.filters import Command
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, InputMediaPhoto
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from bot import dp
from models import Listing, engine


@dp.message(Command('all'))
async def list_my_listings(message: types.Message):
    async with AsyncSession(engine) as session:
        listings = await session.execute(select(Listing))
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
        await message.answer("У вас нет объявлений.")
