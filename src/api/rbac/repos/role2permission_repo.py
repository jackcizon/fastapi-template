from sqlalchemy import values, column, String, tuple_, delete, Select, select
from sqlalchemy.dialects.postgresql import Insert
from sqlalchemy.orm import Session

from src.api.rbac.models import Role2Permission, Role, Permission
from src.core.db.repo.base import ModifyRepo


class Role2PermissionRepo(ModifyRepo):
    def __init__(self, db: Session):
        super().__init__(db)
        self.model = Role2Permission
        self.role = Role
        self.permission = Permission

    def upsert_by_role_perm_pairs(self, role_perm_pairs: list[tuple[str, str]]) -> None:
        # values_clause = ",".join(
        #     f"('{role_name}', '{perm_code}')" for role_name, perm_code in role_perm_pairs
        # )  # ('chairman', 'auth:login'),('ceo', 'auth:login'),('cto', 'auth:login'), ...
        # stat = text(f"""
        #             INSERT INTO "Rbac_Role2Permission"(role_id, permission_id)
        #             SELECT role.id, perm.id
        #             FROM (VALUES {values_clause}) AS tmp(role_name, perm_code)
        #             JOIN "Rbac_Role" role ON role.name = tmp.role_name
        #             JOIN "Rbac_Permission" perm ON perm.code = tmp.perm_code
        #             ON CONFLICT(role_id, permission_id) DO NOTHING;
        #             """)

        tmp_role_perm_pairs_values = values(
            column("role_name", String), column("perm_code", String), name="tmp_role_perm_pairs_values"
        ).data(role_perm_pairs)

        # .c is .column
        stat = (
            select(self.role.id, self.permission.id)
            .select_from(tmp_role_perm_pairs_values)
            .join(self.role, self.role.name == tmp_role_perm_pairs_values.c.role_name)
            .join(self.permission, self.permission.code == tmp_role_perm_pairs_values.c.perm_code)
        )

        stat = Insert(self.model).from_select(["role_id", "permission_id"], stat)
        stat = stat.on_conflict_do_nothing(index_elements=["role_id", "permission_id"])
        self.db.execute(stat)

    def del_dirty_data(self, role_perm_pairs: list[tuple[str, str]]) -> None:
        # values_clause = ",".join(
        #     f"('{role_name}', '{perm_code}')" for role_name, perm_code in role_perm_pairs
        # )  # ('chairman', 'auth:login'),('ceo', 'auth:login'),('cto', 'auth:login'), ...
        # del_dirties = text(f"""
        #                 DELETE FROM "Rbac_Role2Permission"
        #                 WHERE (role_id, permission_id) NOT IN (
        #                 SELECT role.id, perm.id
        #                 FROM (VALUES {values_clause}) AS tmp(role_name, perm_code)
        #                 JOIN "Rbac_Role" role ON role.name = tmp.role_name
        #                 JOIN "Rbac_Permission" perm ON perm.code = tmp.perm_code);
        #                 """)

        tmp_values = values(
            column("role_name", String), column("perm_code", String), name="tmp_role_perm_pairs_values"
        ).data(role_perm_pairs)

        valid_ids_query = (
            Select(self.role.id, self.permission.id)
            .select_from(tmp_values)
            .join(self.role, self.role.name == tmp_values.c.role_name)
            .join(self.permission, self.permission.code == tmp_values.c.perm_code)
        ).scalar_subquery()

        stat = delete(self.model).where(tuple_(self.model.role_id, self.model.permission_id).not_in(valid_ids_query))

        self.db.execute(stat)
