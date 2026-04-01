from sqlalchemy import BigInteger
from sqlalchemy.orm import Mapped, mapped_column

from src.core.db.models import BaseModel


class UserProfile(BaseModel):
    id: Mapped[int] = mapped_column(BigInteger, comment="same as Rbac_User.id", primary_key=True, autoincrement=False)
    # additional fields
