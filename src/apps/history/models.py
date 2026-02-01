from sqlalchemy.sql import func
from sqlalchemy import Column, Integer, ForeignKey, DateTime
from sqlalchemy.orm import relationship

from src.core.database import Base


class BrowseHistory(Base):
    """
    浏览记录
    """

    __tablename__ = "browse_history"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("user.id"))
    book_id = Column(Integer, ForeignKey("book.book_id"))

    book = relationship("Book", uselist=False)
    created = Column(DateTime(), server_default=func.now())
    updated = Column(DateTime(), server_default=func.now())
