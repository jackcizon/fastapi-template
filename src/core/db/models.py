from datetime import datetime

from sqlalchemy import func
from sqlalchemy.orm import Mapped, mapped_column, DeclarativeBase


class Base(DeclarativeBase):
    pass


class BaseModel(Base):
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    # uuid: Mapped[uuid.uuid4()] = mapped_column(primary_key=True)
    created_time: Mapped[datetime] = mapped_column(server_default=func.now())
    is_deleted: Mapped[bool] = mapped_column(default=False, nullable=False)

    __abstract__ = True
