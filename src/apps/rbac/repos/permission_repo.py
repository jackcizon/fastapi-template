from sqlalchemy import text
from sqlalchemy.orm import Session

from src.apps.rbac.models import Permission
from src.core.db.repo.base import ModifyRepo


class PermissionRepo(ModifyRepo):
    def __init__(self, db: Session):
        super().__init__(db, model=Permission)

    def upsert_by_codes(self, codes: list[str]) -> None:
        code_values = ",".join(f"('{code}')" for code in codes)  # ('auth:login'),('auth:register'), ...
        stat = text(f"""
                    INSERT INTO "Rbac_Permission"(code)
                    VALUES {code_values}
                    ON CONFLICT(code) DO NOTHING;
                    """)
        self.db.execute(stat)

    def del_dirty_data(self, codes: list[str]) -> None:
        codes = ",".join(f"'{code}'" for code in codes)  # 'auth:login','auth:register', ...
        stat = text(f"""
                    DELETE FROM "Rbac_Permission"
                    WHERE code NOT IN ({codes});
                    """)
        self.db.execute(stat)
