# ORM things

do not use `fk`, `relationship` and other `so called advanced features` in `sqlalchemy orm`,
just use *_id, do more code logic.

```python
from sqlalchemy import String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from src.core.database import Base


# ================
# 1-1
# ================
class Person(Base):
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(32), index=True)

    __tablename__ = "User1"


class PersonProfile(Base):
    id: Mapped[int] = mapped_column(primary_key=True)
    address: Mapped[str] = mapped_column(String(255))
    person_id: Mapped[int] = mapped_column(index=True, unique=True)

    __tablename__ = "PersonProfile"


# ================
# 1-N
# ================
class Department(Base):
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(32))

    __tablename__ = "Department"


class User(Base):
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(32))
    department_id: Mapped[int] = mapped_column(index=True)

    __tablename__ = "User"


# ================
# N-N
# ================
class Role(Base):
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(32))

    __tablename__ = "Role"


class Permission(Base):
    id: Mapped[int] = mapped_column(primary_key=True)
    code: Mapped[str] = mapped_column(String(64), index=True)

    __tablename__ = "Permission"


class Role2Permission(Base):
    id: Mapped[int] = mapped_column(primary_key=True)
    role_id: Mapped[int] = mapped_column(index=True)
    permission_id: Mapped[int] = mapped_column(index=True)

    __tablename__ = "Role2Permission"
    __table_args__ = (
        UniqueConstraint("role_id", "permission_id", name="unique_role_permission"),
    )
```