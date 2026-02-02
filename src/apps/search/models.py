from sqlalchemy import Column, Integer, String, Boolean

from src.utils.models import BaseModel


class SearchKeyWord(BaseModel):
    """搜索关键词"""

    keyword = Column(String(100))
    count = Column(Integer(), default=0)
    is_hot: bool = Column(Boolean(), default=False)

    __tablename__ = "search_keyword"
