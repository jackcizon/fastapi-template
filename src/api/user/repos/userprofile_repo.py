from typing import Any

from sqlalchemy import Insert
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.user.models import UserProfile
from src.core.db.repo.base import CrudRepo
from src.core.db.repo.mixins import BatchCreateMixin


class UserProfileRepo(BatchCreateMixin, CrudRepo[UserProfile]):
    def __init__(self, db: AsyncSession) -> None:
        super().__init__(db, model=UserProfile)

    async def batch_create(self, params: list[dict[str, Any]] = None) -> None:
        stat = Insert(self.model)
        await self.db.execute(stat, params)
