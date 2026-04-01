from typing import Any

from sqlalchemy.dialects.postgresql import Insert
from sqlalchemy.orm import Session

from src.api.rbac.models import Role
from src.core.db.repo.base import CrudRepo
from src.core.db.repo.mixins import BatchCreateMixin
from src.core.types import Model


class RoleRepo(BatchCreateMixin, CrudRepo[Model]):
    def __init__(self, db: Session) -> None:
        super().__init__(db, model=Role)

    def batch_create(self, params: list[dict[str, Any]] = None) -> None:
        stat = Insert(self.model)
        stat = stat.on_conflict_do_nothing(index_elements=["name"])
        self.db.execute(stat, params)
