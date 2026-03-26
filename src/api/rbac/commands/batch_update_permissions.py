from typing import Any

from click import Command, Context
from fastapi.routing import APIRoute
from starlette.routing import Route

from src.main import app
from src.api.rbac.repos.permission_repo import PermissionRepo
from src.api.rbac.repos.role2permission_repo import Role2PermissionRepo
from src.core.db.session import SessionLocal
from src.core.constants import ROLE_CHILD_MAP, PASSED_APP_PERMISSIONS_CHECK, DEFAULT_ROLE
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
            try:
                # app name must in urlpath, e.g.: app:demo, url:/demo
                app_name = app_route.path.split("/")[1]
            except Exception as e:
                raise e

            if app_name in PASSED_APP_PERMISSIONS_CHECK:
                continue

            code = app_route.name
            metadata: dict[Any, Any] | None = app_route.openapi_extra

            if metadata is None:
                role = DEFAULT_ROLE
            else:
                role = metadata.get("role", DEFAULT_ROLE)

            role_parents_set = get_superior_roles(role, ROLE_CHILD_MAP)

            # permissions.append(PermissionInfo(code=code, role_parents_set=role_parents_set))
            valid_codes.append(code)
            roles_dict[role] = role_parents_set

        with SessionLocal() as db:  # manually manage db context
            try:
                perm_repo = PermissionRepo(db)
                role2perm_repo = Role2PermissionRepo(db)

                if valid_codes is None:
                    perm_repo.del_all()
                    role2perm_repo.del_all()
                    db.commit()
                    return

                perm_repo.upsert_by_codes(valid_codes)
                perm_repo.del_dirty_data(valid_codes)

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

                role2perm_repo.upsert_by_role_perm_pairs(role_perm_pairs)
                role2perm_repo.del_dirty_data(role_perm_pairs)

                # example in django orm: not optimize:
                # for permission in permissions:
                #     code = permission.code
                #     url = permission.url
                #     role_names = permission.role_parents_set
                #     perm, _ = Permission.objects.update_or_create(
                #         code=code,
                #         url=url
                #     )
                #     for role_name in role_names:
                #         role = Role.objects.get(name=role_name)
                #         Role2Permission.objects.update_or_create(
                #             role_id=role.id,
                #             permission_id=perm.id
                #         )

                db.commit()
            except Exception as e:
                db.rollback()
                raise e

        return super().invoke(ctx)
