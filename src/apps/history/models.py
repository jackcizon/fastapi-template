from sqlalchemy.sql import func
from sqlalchemy import Column, Integer, DateTime, Index

from src.utils.models import BaseModel


class BrowseHistory(BaseModel):
    """
    浏览记录
    """

    id = Column(Integer(), primary_key=True)
    user_id = Column(Integer(), index=True)
    book_id = Column(Integer(), index=True)

    created = Column(DateTime(), server_default=func.now())
    updated = Column(DateTime(), server_default=func.now())

    __tablename__ = "browse_history"
    __table_args__ = (Index("ix_user_book", "user_id", "book_id"),)
