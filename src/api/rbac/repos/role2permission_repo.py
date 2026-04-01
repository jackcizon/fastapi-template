from sqlalchemy.orm import Session

from src.api.rbac.models import Role2Permission
from src.core.db.repo.base import CrudRepo


class Role2PermissionRepo(CrudRepo):
    def __init__(self, db: Session):
        super().__init__(db, model=Role2Permission)
