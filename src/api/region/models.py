from sqlalchemy import String, Integer
from sqlalchemy.orm import Mapped, mapped_column

from src.api.region.schemas.enums import RegionType
from src.core.db.mixin import IdMixin
from src.core.db.models import Base


class Region(IdMixin, Base):
    parent_id: Mapped[int] = mapped_column(Integer, index=True, nullable=True)
    name: Mapped[str] = mapped_column(String(32))
    type: Mapped[str] = mapped_column(String(16))

    __tablename__ = "Region"
