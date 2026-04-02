from typing import Any

from sqlalchemy.dialects.postgresql import Insert
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.rbac.models import Role
from src.core.db.repo.base import CrudRepo
from src.core.db.repo.mixins import BatchCreateMixin


class RoleRepo(BatchCreateMixin, CrudRepo[Role]):
    def __init__(self, db: AsyncSession) -> None:
        super().__init__(db, model=Role)

    async def batch_create(self, params: list[dict[str, Any]] = None) -> None:
        stat = Insert(self.model)
        stat = stat.on_conflict_do_nothing(index_elements=["name"])
        await self.db.execute(stat, params)
