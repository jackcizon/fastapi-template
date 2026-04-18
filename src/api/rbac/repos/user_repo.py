from typing import Any

from sqlalchemy import select, text
from sqlalchemy.dialects.postgresql import Insert
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.rbac.models import User
from src.core.db.repo.base import CrudRepo
from src.core.db.repo.mixins import BatchCreateMixin


class UserRepo(BatchCreateMixin, CrudRepo[User]):
    def __init__(self, db: AsyncSession) -> None:
        super().__init__(db, model=User)

    async def get_one_by_field_eq(self, field: str, val: Any) -> User | None:
        stat = (
            select(self.model)
            .where(self.column(field) == val)  # type: ignore
            .where(self.model.is_deleted.is_(False))
        )

        res = await self.db.execute(stat)
        return res.scalars().first()

    async def batch_create(self, params: list[dict[str, Any]] = None) -> None:
        stat = Insert(self.model)
        stat = stat.on_conflict_do_nothing(index_elements=["email"], index_where=text("is_deleted IS FALSE"))
        await self.db.execute(stat, params)
