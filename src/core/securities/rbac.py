from typing import Any, Sequence

from fastapi import HTTPException, Request, Depends
from fastapi.routing import APIRoute
from sqlalchemy.orm import Session

from src.api.rbac.models import User
from src.api.rbac.repos.rbac_repo import RbacRepo
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


class RolePermissionCheck:
    def __init__(self) -> None:
        self._user: User | None = None
        self._permission_code: str | None = None
        self._role: str | None = None
        self._passed: bool = False  # state

    async def _assign_args(self, request: Request, user: User) -> None:
        self._user = user
        route: APIRoute = request.scope.get("route")
        self._permission_code = route.name
        metadata: dict[Any, Any] | None = route.openapi_extra
        if metadata is None:
            self._role = DEFAULT_ROLE
        else:
            self._role = metadata.get("role")

    def _has_permission(self, db: Session, user: User) -> bool:
        user_permissions: Sequence[str] = RbacRepo(db).get_user_permissions(user)
        codes: list[str] = [user_permission for user_permission in user_permissions]

        if self._permission_code in codes:
            self._passed = True
        return self._passed

    def _result(self) -> tuple[User, str]:
        return self._user, self._role

    async def __call__(
        self,
        request: Request,
        db: Session,  # can del Depends, avoid repeat params
        user: User,  # can del Depends, avoid repeat params
    ) -> tuple[User, str]:
        await self._assign_args(request, user)
        if not self._has_permission(db, user):
            raise HTTPException(status_code=403, detail="403 Forbidden")
        return self._result()


async def role_prem_check_wrapper_dep(
    request: Request, db: Session = Depends(get_db), user: User = Depends(jwt_required_dep)
):
    checker = RolePermissionCheck()
    return await checker(request, db, user)
