from sqlalchemy import String, UniqueConstraint, BigInteger, Integer
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.orm import Mapped, mapped_column

from src.core.db.mixin import IdMixin, DistributedIdMixin
from src.core.db.models import BaseModel, Base
from src.core.db.session import SessionLocal
from src.core.securities.password import Password


class Role(IdMixin, Base):
    name: Mapped[str] = mapped_column(String(16), unique=True)

    __tablename__ = "Rbac_Role"


class Permission(IdMixin, Base):
    code: Mapped[str] = mapped_column(String(256), unique=True)

    __tablename__ = "Rbac_Permission"


class User(DistributedIdMixin, BaseModel):
    name: Mapped[str] = mapped_column(String(16))
    email: Mapped[str] = mapped_column(String(32), nullable=False, unique=True)
    password: Mapped[str] = mapped_column(String(256))

    __tablename__ = "Rbac_User"


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


# if __name__ == "__main__":
#     with SessionLocal() as db:
#         try:
#             params = [{"name": "jack", "email": "jack@qq.com", "password": Password.hash("123456")}]
#             stat = insert(User).on_conflict_do_nothing(index_elements=["email"]).returning(User)
#             user = db.execute(stat, params).scalars().first()
#
#             if user:
#                 params = [{"user_id": user.id, "role_id": 68}]
#                 stat = insert(User2Role)
#                 db.execute(stat, params)
#                 db.commit()
#         except Exception as e:
#             db.rollback()
#             raise e
