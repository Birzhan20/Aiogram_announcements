from datetime import datetime

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Integer, String, Float, Text, Boolean, DateTime


DATABASE_URL = "sqlite+aiosqlite:///4you.db"

engine = create_async_engine(DATABASE_URL, echo=True)
Base = declarative_base()
SessionLocal = async_sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)


class Listing(Base):
    __tablename__ = 'listings'

    id = Column(Integer, primary_key=True, index=True)
    model = Column(String, index=True)
    condition = Column(String)
    price = Column(Float)
    description = Column(Text)
    photo1 = Column(String)
    photo2 = Column(String)
    photo3 = Column(String)
    is_active = Column(Boolean, default=True)
    date_added = Column(DateTime, default=datetime.utcnow)
    seller_username = Column(String, nullable=False)
