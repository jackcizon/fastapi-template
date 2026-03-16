from typing import Any

from fastapi.routing import APIRoute
from starlette.routing import Route

from src.main import app
from src.utils.constants import ROLE_CHILD_MAP, PASSED_APP_PERMISSIONS_CHECK
from src.utils.datastructures.permission_info import PermissionInfo
from src.utils.helpers import get_superior_roles


def batch_update_permissions():
    permissions: list[PermissionInfo] = []
    app_routes: list[Route | APIRoute | Any] = app.instance.routes
    for app_route in app_routes:
        # pass some fastapi built-in routes like 'openapi, swagger, redoc'
        if not isinstance(app_route, APIRoute):
            continue

        # auth app must pass
        app_name = app_route.path.split('/')[1]
        if app_name in PASSED_APP_PERMISSIONS_CHECK:
            continue

        code = app_route.name
        metadata: dict[str, str] | None = app_route.openapi_extra

        if metadata is None:
            role = 'user'
        else:
            role = metadata.get('role', 'user')

        role_parents_set = get_superior_roles(role, ROLE_CHILD_MAP)

        permissions.append(
            PermissionInfo(code=code, role_parents_set=role_parents_set)
        )

        for p in permissions:
            print(f'{p.role_parents_set} => {p.code}')


if __name__ == '__main__':
    batch_update_permissions()
