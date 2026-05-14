from sqlalchemy import BigInteger, String, Integer
from sqlalchemy.orm import Mapped, mapped_column

from src.api.region.schemas.enums import RegionType
from src.core.db.mixin import DistributedIdMixin
from src.core.db.models import BaseModel, Base


class UserProfile(BaseModel):
    id: Mapped[int] = mapped_column(BigInteger, comment="same as Rbac_User.id", primary_key=True, autoincrement=False)
    avatar: Mapped[str] = mapped_column(String(256), default="static/media/avatar/default_avatar.png")

    __tablename__ = "UserProfile"


class UserAddress(DistributedIdMixin, Base):
    user_id: Mapped[int] = mapped_column(BigInteger, index=True)
    country_id: Mapped[int] = mapped_column(Integer, index=True)
    region_id: Mapped[int] = mapped_column(Integer, index=True)
    detail_address: Mapped[str] = mapped_column(String(64), default=RegionType.unknown)
    postal_code: Mapped[str] = mapped_column(String(16))

    __tablename__ = "UserAddress"
