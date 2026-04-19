from sqlalchemy.ext.asyncio import AsyncSession

from src.api.rbac.models import User2Role
from src.core.db.repo.base import QueryRepo
from src.core.db.repo.mixins import BatchCreateMixin


class User2RoleRepo(BatchCreateMixin, QueryRepo[User2Role]):
    def __init__(self, db: AsyncSession) -> None:
        super().__init__(db, model=User2Role)
