from aiogram import types
from aiogram.enums import ParseMode
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from bot import dp
from core.config import AsyncSessionLocal
from models import Listing


# Функция для выборки данных с LIMIT и OFFSET
async def get_listings(session: AsyncSession, limit: int = 10, offset: int = 0):
    query = select(Listing).limit(limit).offset(offset)
    result = await session.execute(query)
    return result.scalars().all()


# Функция для добавления данных в базу
async def insert_data(session: AsyncSession, data: list):
    try:
        for item in data:
            listing = Listing(id=item['id'], answer=item['answer'])
            session.add(listing)
        await session.commit()
        print("Данные были успешно добавлены в базу.")
    except Exception as e:
        print(f"Ошибка при добавлении данных: {e}")
        await session.rollback()  # Откатываем изменения в случае ошибки


# Функция для проверки, существует ли таблица
async def is_db_populated(session: AsyncSession):
    result = await session.execute(select(Listing).limit(1))  # Запрос с select
    count = len(result.scalars().all())  # Получаем количество записей
    return count > 0  # Если записи есть, возвращаем True


# Получение ответа по ID
async def get_answer_by_id(session: AsyncSession, question_id: int):
    query = select(Listing).filter(Listing.id == question_id)
    result = await session.execute(query)
    listing = result.scalars().first()  # Получаем первую запись (если есть)
    return listing.answer if listing else None  # Возвращаем ответ или None


# Функция для получения списка всех ID из базы данных
async def get_all_ids(session):
    query = select(Listing.id)
    result = await session.execute(query)
    ids = result.scalars().all()
    return ids


@dp.callback_query(lambda callback: callback.data.isdigit())
async def process_question(callback: types.CallbackQuery):
    async with AsyncSessionLocal() as session:
        all_ids = await get_all_ids(session)  # Получаем все ID из базы данных
        question_id = int(callback.data)
        if question_id in all_ids:  # Проверяем, существует ли ID
            answer = await get_answer_by_id(session, question_id)  # Получаем ответ из базы данных

            if answer:
                await callback.answer("Ответ найден.", show_alert=True)
                await callback.message.edit_text(
                    f"Ответ на ваш вопрос:\n\n{answer}",
                    parse_mode=ParseMode.HTML
                )
            else:
                await callback.answer("Извините, ответ не найден.", show_alert=True)
                await callback.message.edit_text(
                    "Мы не нашли ответа на ваш вопрос. Пожалуйста, попробуйте позже.",
                    parse_mode=ParseMode.HTML
                )
        else:
            await callback.answer("Неверный ID.", show_alert=True)
            await callback.message.edit_text(
                "ID не найден в базе данных.",
                parse_mode=ParseMode.HTML
            )
