from sqlalchemy import BigInteger, String
from sqlalchemy.orm import Mapped, mapped_column

from src.core.db.models import BaseModel


class UserProfile(BaseModel):
    id: Mapped[int] = mapped_column(BigInteger, comment="same as Rbac_User.id", primary_key=True, autoincrement=False)
    avatar: Mapped[str] = mapped_column(String(256), default="static/media/avatar/default_avatar.png")

    __tablename__ = "UserProfile"
