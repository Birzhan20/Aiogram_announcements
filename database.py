from aiogram.fsm.context import FSMContext
from sqlalchemy.ext.asyncio import AsyncSession
from models import engine, Listing


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
