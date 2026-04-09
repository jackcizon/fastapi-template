from sqlalchemy import String, UniqueConstraint, BigInteger, Integer, text, Index
from sqlalchemy.orm import Mapped, mapped_column

from src.core.db.mixin import IdMixin, DistributedIdMixin
from src.core.db.models import BaseModel, Base


class Role(IdMixin, Base):
    name: Mapped[str] = mapped_column(String(16), unique=True)

    __tablename__ = "Rbac_Role"


class Permission(IdMixin, Base):
    code: Mapped[str] = mapped_column(String(256), unique=True)

    __tablename__ = "Rbac_Permission"


class User(DistributedIdMixin, BaseModel):
    name: Mapped[str] = mapped_column(String(16))
    email: Mapped[str] = mapped_column(String(32), nullable=False)
    password: Mapped[str] = mapped_column(String(256))

    __tablename__ = "Rbac_User"
    __table_args__ = (
        # # partial index
        # email is unique globally.
        # enable reuse: if a user is deleted, his email can be reused, system can create a new user with same email.
        Index("unique_user_email_active", "email", unique=True, postgresql_where=text("is_deleted IS FALSE")),
    )


class User2Role(DistributedIdMixin, Base):
    """no fk constraint, but do more works."""

    user_id: Mapped[int] = mapped_column(BigInteger, index=True)
    role_id: Mapped[int] = mapped_column(Integer, index=True)

    __tablename__ = "Rbac_User2Role"
    __table_args__ = (UniqueConstraint("user_id", "role_id", name="unique_user_role"),)


class Role2Permission(IdMixin, Base):
    role_id: Mapped[int] = mapped_column(Integer, index=True)
    permission_id: Mapped[int] = mapped_column(Integer, index=True)

    __tablename__ = "Rbac_Role2Permission"
    __table_args__ = (UniqueConstraint("role_id", "permission_id", name="unique_role_permission"),)
