from sqlalchemy import text
from sqlalchemy.orm import Session

from src.apps.rbac.models import Role2Permission
from src.core.db.repo.base import ModifyRepo


class Role2PermissionRepo(ModifyRepo):
    def __init__(self, db: Session):
        super().__init__(db, model=Role2Permission)

    def upsert_by_role_perm_pairs(self, role_perm_pairs: list[tuple[str, str]]) -> None:
        values_clause = ",".join(
            f"('{role_name}', '{perm_code}')" for role_name, perm_code in role_perm_pairs
        )  # ('chairman', 'auth:login'),('ceo', 'auth:login'),('cto', 'auth:login'), ...
        stat = text(f"""
                    INSERT INTO "Rbac_Role2Permission"(role_id, permission_id)
                    SELECT role.id, perm.id
                    FROM (VALUES {values_clause}) AS tmp(role_name, perm_code)
                    JOIN "Rbac_Role" role ON role.name = tmp.role_name
                    JOIN "Rbac_Permission" perm ON perm.code = tmp.perm_code
                    ON CONFLICT(role_id, permission_id) DO NOTHING;
                    """)
        self.db.execute(stat)

    def del_dirty_data(self, role_perm_pairs: list[tuple[str, str]]) -> None:
        values_clause = ",".join(
            f"('{role_name}', '{perm_code}')" for role_name, perm_code in role_perm_pairs
        )  # ('chairman', 'auth:login'),('ceo', 'auth:login'),('cto', 'auth:login'), ...
        del_dirties = text(f"""
                        DELETE FROM "Rbac_Role2Permission"
                        WHERE (role_id, permission_id) NOT IN (
                        SELECT role.id, perm.id
                        FROM (VALUES {values_clause}) AS tmp(role_name, perm_code)
                        JOIN "Rbac_Role" role ON role.name = tmp.role_name
                        JOIN "Rbac_Permission" perm ON perm.code = tmp.perm_code);
                        """)
        self.db.execute(del_dirties)
