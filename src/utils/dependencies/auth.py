from typing import Any

from fastapi import HTTPException, Request, Depends
from fastapi.routing import APIRoute
from jwt import ExpiredSignatureError, InvalidTokenError
from sqlalchemy.orm import Session

from src.apps.rbac.models import User
from src.apps.rbac.repos import UserRepo, RbacRepo
from src.apps.rbac.services import UserService, RbacService
from src.core.database import get_db, SessionLocal
from src.utils.constants import DEFAULT_ROLE
from src.utils.datastructures.json_web_token import JSONWebToken


def jwt_required_dep(request: Request) -> User:
    """
    :param request: FastAPI Request
    :return: str: user_id
    """
    auth = request.headers.get("Authorization")
    if not auth or not auth.startswith("Bearer "):
        raise HTTPException(401, "Not authenticated")

    token = auth.split(" ")[1]

    try:
        payload = JSONWebToken.decode_token(token)
    except ExpiredSignatureError:
        raise HTTPException(401, "Token expired")
    except InvalidTokenError:
        raise HTTPException(401, "Invalid token")

    # 2. payload type check
    if payload.get("type") != "access":
        raise HTTPException(status_code=401, detail="token type must be access")
    user_id = payload.get("user_id")

    with SessionLocal() as db:
        try:
            user = UserService(UserRepo(db)).get_user_by_id(user_id)
        except Exception as e:
            print(e)
            db.rollback()
            raise
        finally:
            db.close()

    if not user_id or user is None:
        raise HTTPException(401, "Invalid token payload")

    return user


class RolePermissionCheck:
    """
    :return: tuple(user_instance, min_req_role_str)
    """

    def __init__(self) -> None:
        self._user: User | None = None
        self._permission_code: str | None = None
        self._role: str | None = None
        self._passed: bool = False

    def assign_args(self, request: Request, user: User) -> None:
        self._user = user
        route: APIRoute = request.scope.get("route")
        self._permission_code = route.name
        metadata: dict[Any, Any] | None = route.openapi_extra
        if metadata is None:
            self._role = DEFAULT_ROLE
        else:
            self._role = metadata.get("role")

    def _has_permission(self, db: Session, user: User) -> bool:
        # TODO: store in cache, query from cache, not db.
        user_permissions = RbacService(RbacRepo(db)).get_user_permissions(user)
        codes = [user_permission[0] for user_permission in user_permissions]

        if self._permission_code in codes:
            self._passed = True
        return self._passed

    def _result(self) -> tuple[User, str]:
        return self._user, self._role

    def __call__(
        self,
        request: Request,
        db: Session = Depends(get_db),
        user: User = Depends(jwt_required_dep),
    ) -> tuple[User, str]:
        self.assign_args(request, user)
        if not self._has_permission(db, user):
            raise HTTPException(status_code=403, detail="403 Forbidden")
        return self._result()
