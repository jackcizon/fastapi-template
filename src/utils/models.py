from sqlalchemy import Column, Integer, Boolean, DateTime, func
from sqlalchemy.orm import Mapped

from src.core.database import Base


class BaseModel(Base):
    id = Column(Integer(), primary_key=True)
    created_time = Column(DateTime(), server_default=func.now())
    is_deleted: Mapped[bool] = Column(Boolean(), default=False, nullable=False)

    __abstract__ = True
