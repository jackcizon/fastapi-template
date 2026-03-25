from typing import Any

from fastapi import HTTPException, Request, Depends
from fastapi.routing import APIRoute
from sqlalchemy.orm import Session

from src.apps.rbac.models import User
from src.apps.rbac.repos.rbac_repo import RbacRepo
from src.core.db.session import get_db
from src.core.securities.jwt import jwt_required_dep
from src.core.constants import DEFAULT_ROLE


def role_permission_check_dep(
        request: Request,
        db: Session = Depends(get_db),
        user: User = Depends(jwt_required_dep),
) -> tuple[User, str]:
    """
    :return: tuple(user_instance, min_req_role_str)
    """
    route: APIRoute = request.scope.get("route")
    permission_code = route.name
    metadata: dict[Any, Any] | None = route.openapi_extra
    if metadata is None:
        role = DEFAULT_ROLE
    else:
        role = metadata.get("role")

    user_permissions = RbacRepo(db).get_user_permissions(user)
    codes = [user_perm for user_perm in user_permissions]
    if permission_code not in codes:
        raise HTTPException(status_code=403, detail="403 Forbidden")
    return user, role
