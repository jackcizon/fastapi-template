from sqlalchemy.ext.asyncio import AsyncSession

from src.api.rbac.models import Permission
from src.core.db.repo.base import CrudRepo
from src.core.db.repo.mixins import BatchCreateMixin


class PermissionRepo(BatchCreateMixin, CrudRepo[Permission]):
    def __init__(self, db: AsyncSession) -> None:
        super().__init__(db, model=Permission)
