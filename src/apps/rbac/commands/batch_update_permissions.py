from typing import Any

from click import Command, Context
from fastapi.routing import APIRoute
from sqlalchemy import text
from starlette.routing import Route

from src.apps.rbac.repos import PermissionRepo, Role2PermissionRepo
from src.apps.rbac.services import PermissionService, Role2PermissionService
from src.core.database import SessionLocal
from src.main import app
from src.utils.constants import ROLE_CHILD_MAP, PASSED_APP_PERMISSIONS_CHECK
from src.utils.helpers import get_superior_roles


class BatchUpdatePermissionsCommand(Command):
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self.help = "batch update rbac permissions"

    def invoke(self, ctx: Context) -> Any:
        # permissions: list[PermissionInfo] = []
        valid_codes: list[str] = []
        roles_dict: dict[str, set[str]] = {}

        app_routes: list[Route | APIRoute | Any] = app.instance.routes
        for app_route in app_routes:
            # pass some fastapi built-in routes like 'openapi, swagger, redoc'
            if not isinstance(app_route, APIRoute):
                continue

            # auth app must pass
            app_name = app_route.path.split("/")[
                1
            ]  # app name must in urlpath, e.g.: app:demo, url:/demo
            if app_name in PASSED_APP_PERMISSIONS_CHECK:
                continue

            code = app_route.name
            metadata: dict[Any, Any] | None = app_route.openapi_extra

            if metadata is None:
                role = "user"
            else:
                role = metadata.get("role", "user")

            role_parents_set = get_superior_roles(role, ROLE_CHILD_MAP)

            # permissions.append(PermissionInfo(code=code, role_parents_set=role_parents_set))
            valid_codes.append(code)
            roles_dict[role] = role_parents_set

        with SessionLocal() as db:
            try:
                if valid_codes is None:
                    PermissionService(PermissionRepo(db)).del_all()
                    Role2PermissionService(Role2PermissionRepo(db)).del_all()
                    db.commit()
                    return

                # upsert Permission
                # code_values = ",".join(
                #     f"('{code}')" for code in valid_codes
                # )  # ('auth:login'),('auth:register'), ...
                # upsert = text(f"""
                # INSERT INTO "Rbac_Permission"(code)
                # VALUES {code_values}
                # ON CONFLICT(code) DO NOTHING;
                # """)
                # db.execute(upsert)
                PermissionService(PermissionRepo(db)).upsert_by_codes(valid_codes)

                # del dirty data
                # codes = ",".join(
                #     f"'{code}'" for code in valid_codes
                # )  # 'auth:login','auth:register', ...
                # del_dirties = text(f"""
                # DELETE FROM "Rbac_Permission"
                # WHERE code NOT IN ({codes});
                # """)
                # db.execute(del_dirties)
                PermissionService(PermissionRepo(db)).del_dirty_data(valid_codes)

                # Role2Permission
                role_perm_pairs: list[tuple[str, str]] = []
                for code in valid_codes:
                    for role, parents in roles_dict.items():
                        for parent_role in parents:
                            # [('cto', 'auth:login'), ('user', 'auth:login'), ('staff', 'auth:login'), ...]
                            role_perm_pairs.append((parent_role, code))

                if not role_perm_pairs:
                    db.commit()
                    return

                # update Role2Permission
                # values_clause = ",".join(
                #     f"('{role_name}', '{perm_code}')" for role_name, perm_code in role_perm_pairs
                # )  # ('chairman', 'auth:login'),('ceo', 'auth:login'),('cto', 'auth:login'), ...
                # upsert = text(f"""
                # INSERT INTO "Rbac_Role2Permission"(role_id, permission_id)
                # SELECT role.id, perm.id
                # FROM (VALUES {values_clause}) AS tmp(role_name, perm_code)
                # JOIN "Rbac_Role" role ON role.name = tmp.role_name
                # JOIN "Rbac_Permission" perm ON perm.code = tmp.perm_code
                # ON CONFLICT(role_id, permission_id) DO NOTHING;
                # """)
                # db.execute(upsert)
                Role2PermissionService(Role2PermissionRepo(db)).upsert_by_list_of_pairs(role_perm_pairs)

                # del dirty data
                # values_clause = ",".join(
                #     f"('{role_name}', '{perm_code}')" for role_name, perm_code in role_perm_pairs
                # )  # ('chairman', 'auth:login'),('ceo', 'auth:login'),('cto', 'auth:login'), ...
                # del_dirties = text(f"""
                # DELETE FROM "Rbac_Role2Permission"
                # WHERE (role_id, permission_id) NOT IN (
                # SELECT role.id, perm.id
                # FROM (VALUES {values_clause}) AS tmp(role_name, perm_code)
                # JOIN "Rbac_Role" role ON role.name = tmp.role_name
                # JOIN "Rbac_Permission" perm ON perm.code = tmp.perm_code);
                # """)
                # db.execute(del_dirties)
                Role2PermissionService(Role2PermissionRepo(db)).del_dirty_data(role_perm_pairs)

                db.commit()
            except Exception as e:
                db.rollback()
                raise e

        return super().invoke(ctx)
