from sqlalchemy import Column, Integer, String, Boolean

from src.core.database import Base


class SearchKeyWord(Base):
    """
    搜索关键词
    """

    __tablename__ = "search_key_word"
    id = Column(Integer(), primary_key=True)
    keyword = Column(String(100))
    count = Column(Integer(), default=0)
    is_hot = Column(Boolean, default=False)
