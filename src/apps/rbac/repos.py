from typing import Sequence, Any

from sqlalchemy import text, Result
from sqlalchemy.dialects.postgresql import Insert
from sqlalchemy.orm import Session

from src.apps.rbac.models import User, Role
from src.core.db.base_repo import BaseRepo


class RoleRepo(BaseRepo):
    def __init__(self, db: Session) -> None:
        super().__init__(db, model=Role)

    def batch_create(self, params: list[dict[str, Any]] = None) -> None:
        stat = Insert(self.model)
        stat = stat.on_conflict_do_nothing(index_elements=["name"])
        self.db.execute(stat, params)


class UserRepo(BaseRepo):
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


class PermissionRepo:
    def __init__(self, db: Session) -> None:
        self.db = db

    def del_all(self) -> None:
        stat = text("""DELETE FROM "Rbac_Permission" where id > 0;""")
        self.db.execute(stat)

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


class Role2PermissionRepo:
    def __init__(self, db: Session) -> None:
        self.db = db

    def del_all(self) -> None:
        stat = text("""DELETE FROM "Rbac_Role2Permission" where id > 0;""")
        self.db.execute(stat)

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


class RbacRepo:
    def __init__(self, db: Session | None = None):
        self.db = db

    def get_user_permissions(self, user: User) -> Sequence:
        user_permissions_result: Result = self.db.execute(
            text("""
                            WITH user_roles AS (
                                SELECT ur.user_id, ur.role_id
                                FROM "Rbac_User2Role" ur
                                WHERE ur.user_id = :user_id
                            ),
                            role_permissions AS (
                                SELECT rp.role_id, rp.permission_id
                                FROM "Rbac_Role2Permission" rp
                                WHERE rp.role_id IN (SELECT role_id FROM user_roles)
                            )
                            SELECT p.code
                            FROM "Rbac_Permission" p
                            JOIN role_permissions rp ON rp.permission_id = p.id;
                            """),
            {"user_id": user.id},
        )
        # [('rbac:index',), ('auth:me',), ('auth:register',), ('auth:login',), ...]
        return user_permissions_result.fetchall()
