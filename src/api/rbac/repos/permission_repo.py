from sqlalchemy.ext.asyncio import AsyncSession

from src.api.rbac.models import Permission
from src.core.db.repo.base import CrudRepo
from src.core.types import Model


class PermissionRepo(CrudRepo[Model]):
    def __init__(self, db: AsyncSession) -> None:
        super().__init__(db, model=Permission)
