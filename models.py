from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Integer, String


DATABASE_URL = "sqlite+aiosqlite:///MyTrade.db"

engine = create_async_engine(DATABASE_URL, echo=True)
Base = declarative_base()
SessionLocal = async_sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)


class Listing(Base):
    __tablename__ = 'listings'

    id = Column(Integer, primary_key=True, index=True)
    answer = Column(String, index=True)

async def add_items():
    async with SessionLocal() as session:
        async with session.begin():
            for _ in range(50):
                item = Listing(answer="in process")
                session.add(item)
        await session.commit()
    print("50 элементов добавлены.")

async def main():
    await add_items()