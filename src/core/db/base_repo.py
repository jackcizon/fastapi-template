from typing import Any

from sqlalchemy import insert
from sqlalchemy.orm import Session


class BaseRepo:
    def __init__(self, model: Any, db: Session):
        self.model = model
        self.db = db

    def get_by_id(self, id_: int) -> Any:
        return self.db.query(self.model).get(id_)

    def batch_create(self, stat: Any, params: list[dict[str, Any]]) -> None:
        if stat is None:
            stat = insert(self.model)
        if params is None:
            params = []
        self.db.execute(stat, params)
