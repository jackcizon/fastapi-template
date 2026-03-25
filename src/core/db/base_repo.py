from typing import Any

from sqlalchemy.orm import Session


class BaseRepo:
    def __init__(self, db: Session, /, *, model: Any = None):
        self.db = db
        self.model = model

    def get_by_id(self, id_: int) -> Any:
        return self.db.query(self.model).get(id_)

    def batch_create(self, params: list[dict[str, Any]] = None) -> None:
        raise NotImplementedError
