from typing import Any, Generic, Sequence

from sqlalchemy import delete, select
from sqlalchemy.orm import Session

from src.core.types import Model


class BaseRepo(Generic[Model]):
    def __init__(self, db: Session, /, *, model: type[Model] = None):
        self.db = db
        self.model = model

    def column(self, field: str) -> Any:
        return getattr(self.model, field)


class QueryRepo(BaseRepo[Model]):
    """select"""

    def get_one_by_field_eq(self, field: str, val: str) -> Model:
        stat = select(self.model).where(self.column(field) == val)  # type: ignore
        return self.db.execute(stat).scalars().first()

    def get_all_by_field_eq(self, field: str, val: str) -> Sequence[Model]:
        stat = select(self.model).where(self.column(field) == val)  # type: ignore
        return self.db.execute(stat).scalars().all()

    def get_all_by_field_in(self, field: str, vals: list[str]) -> Sequence[Model]:
        col = getattr(self.model, field)
        stat = select(self.model).where(col.in_(vals))
        return self.db.execute(stat).scalars().all()


class ModifyRepo(BaseRepo[Model]):
    """update, delete, insert"""

    def del_all(self) -> None:
        stat = delete(self.model).where(self.column("id") > 0)
        self.db.execute(stat)


class CrudRepo(QueryRepo[Model], ModifyRepo[Model]):
    """crud"""

    def execute_stat_params(self, stat: Any, params: list[dict[str, Any]] = None) -> Any:
        return self.db.execute(stat, params)
