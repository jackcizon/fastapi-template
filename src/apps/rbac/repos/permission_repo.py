from sqlalchemy import text, delete
from sqlalchemy.orm import Session
from sqlalchemy.dialects.postgresql.dml import Insert

from src.apps.rbac.models import Permission
from src.core.db.repo.base import ModifyRepo


class PermissionRepo(ModifyRepo):
    def __init__(self, db: Session):
        super().__init__(db)  # write in super.init() won't gain type hint
        self.model = Permission  # write here will gain type hint

    def upsert_by_codes(self, codes: list[str]) -> None:
        # code_values = ",".join(f"('{code}')" for code in codes)  # ('auth:login'),('auth:register'), ...
        # stat = text(f"""
        #             INSERT INTO "Rbac_Permission"(code)
        #             VALUES {code_values}
        #             ON CONFLICT(code) DO NOTHING;
        #             """)

        params = []
        for code in codes:
            params.append({"code": code})

        stat = Insert(self.model)
        stat = stat.on_conflict_do_nothing(index_elements=["code"])
        self.db.execute(stat, params)

    def del_dirty_data(self, codes: list[str]) -> None:
        # codes = ",".join(f"'{code}'" for code in codes)  # 'auth:login','auth:register', ...
        # stat = text(f"""
        #             DELETE FROM "Rbac_Permission"
        #             WHERE code NOT IN ({codes});
        #             """)

        params = []
        for code in codes:
            params.append({"code": code})

        stat = delete(self.model).where(~self.model.code.in_(codes))
        self.db.execute(stat)
