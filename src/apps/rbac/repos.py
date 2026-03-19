from sqlalchemy import text
from sqlalchemy.orm import Session


class UserRepo:
    def __init__(self, db: Session | None = None) -> None:
        self.db = db

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
        result = self.db.execute(statement=stat, params={"email": email}).mappings().first()
        return result


class PermissionRepo:
    def __init__(self, db: Session) -> None:
        self.db = db

    def del_all(self) -> None:
        stat = text("""DELETE FROM "Rbac_Permission" where id > 0;""")
        self.db.execute(stat)

    def upsert_by_codes(self, codes: list[str]) -> None:
        code_values = ",".join(
            f"('{code}')" for code in codes
        )  # ('auth:login'),('auth:register'), ...
        stat = text(f"""
                        INSERT INTO "Rbac_Permission"(code)
                        VALUES {code_values}
                        ON CONFLICT(code) DO NOTHING;
                        """)
        self.db.execute(stat)

    def del_dirty_data(self, codes: list[str]):
        codes = ",".join(
            f"'{code}'" for code in codes
        )  # 'auth:login','auth:register', ...
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

    def del_dirty_data(self, role_perm_pairs):
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
