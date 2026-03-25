from typing import Any

from sqlalchemy import delete
from sqlalchemy.orm import Session


class BaseRepo:
    def __init__(self, db: Session, /, *, model: Any = None):
        self.db = db
        self.model = model


class QueryRepo(BaseRepo):
    """select"""

    def get_by_id(self, id_: int) -> Any:
        return self.db.query(self.model).get(id_)


class ModifyRepo(BaseRepo):
    """update, delete, insert"""

    def del_all(self) -> None:
        stat = delete(self.model).where(self.model.id > 0)
        self.db.execute(stat)


class CrudRepo(ModifyRepo):
    """crud"""
    pass
