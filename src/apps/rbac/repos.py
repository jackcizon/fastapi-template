from typing import Any

from sqlalchemy import text
from sqlalchemy.orm import Session


class UserRepo:
    def __init__(self, db: Session | None = None) -> None:
        self.db = db

    def get_user_by_email(self, email: str) -> dict[str, str] | None:
        """
        :return: dict(name, email, password) or None
        """
        stat = text("""
            select id, name, password, email
            from "Rbac_User"
            where email = :email
              and is_deleted = false;
            """)
        result = self.db.execute(statement=stat, params={"email": email}).mappings().first()
        return result
