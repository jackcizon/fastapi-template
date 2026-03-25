from typing import Any

from sqlalchemy import text
from sqlalchemy.dialects.postgresql import Insert
from sqlalchemy.orm import Session

from src.apps.rbac.models import User
from src.core.db.repo.base import QueryRepo
from src.core.db.repo.mixins import BatchCreateMixin


class UserRepo(BatchCreateMixin, QueryRepo):
    def __init__(self, db: Session) -> None:
        super().__init__(db, model=User)

    def get_user_by_email(self, email: str) -> dict[str, str] | None:
        """
        :return: dict(id, name, email, password) or None
        """
        stat = text("""
                    select id, name, password, email
                    from "Rbac_User"
                    where email = :email
                      and is_deleted = false;
                    """)
        result = self.db.execute(stat, {"email": email}).mappings().first()
        return result

    def batch_create(self, params: list[dict[str, Any]] = None) -> None:
        stat = Insert(self.model)
        stat = stat.on_conflict_do_nothing(index_elements=["email"])
        self.db.execute(stat, params)
