from sqlalchemy.ext.asyncio import AsyncSession

from src.api.rbac.models import Role2Permission
from src.core.db.repo.base import CrudRepo


class Role2PermissionRepo(CrudRepo[Role2Permission]):
    def __init__(self, db: AsyncSession):
        super().__init__(db, model=Role2Permission)
