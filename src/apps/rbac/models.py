from sqlalchemy import String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from src.core.db.session import Base
from src.utils.models import BaseModel


class Role(Base):
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(16), unique=True)

    __tablename__ = "Rbac_Role"


class Permission(Base):
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    code: Mapped[str] = mapped_column(String(256), unique=True)

    __tablename__ = "Rbac_Permission"


class User(BaseModel):
    name: Mapped[str] = mapped_column(String(16))
    email: Mapped[str] = mapped_column(String(32), nullable=False, unique=True)
    password: Mapped[str] = mapped_column(String(256))

    __tablename__ = "Rbac_User"


class User2Role(Base):
    """no fk constraint, but do more works."""

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(index=True)
    role_id: Mapped[int] = mapped_column(index=True)

    __tablename__ = "Rbac_User2Role"
    __table_args__ = (UniqueConstraint("user_id", "role_id", name="unique_user_role"),)


class Role2Permission(Base):
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    role_id: Mapped[int] = mapped_column(index=True)
    permission_id: Mapped[int] = mapped_column(index=True)

    __tablename__ = "Rbac_Role2Permission"
    __table_args__ = (UniqueConstraint("role_id", "permission_id", name="unique_role_permission"),)
