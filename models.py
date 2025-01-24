from sqlalchemy import Column, Integer, String, select
from core.config import Base


class Listing(Base):
    __tablename__ = 'listings'

    id = Column(Integer, primary_key=True, index=True)
    answer = Column(String, index=True)
