from sqlalchemy.orm import Session

from src.api.rbac.models import Permission
from src.core.db.repo.base import CrudRepo
from src.core.types import Model


class PermissionRepo(CrudRepo[Model]):
    def __init__(self, db: Session) -> None:
        super().__init__(db, model=Permission)
