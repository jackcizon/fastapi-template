from fastapi import APIRouter
from fastapi.params import Depends
from starlette.responses import JSONResponse

from src.apps.rbac.models import User
from src.utils.dependencies.auth import RolePermissionCheck

rbac_router = APIRouter()


@rbac_router.get("/index/", name="rbac:index", openapi_extra={"role": "staff"})
def rbac_index(user_role: tuple[User, str] = Depends(RolePermissionCheck())) -> JSONResponse:
    user, role = user_role
    return JSONResponse(content={"user": user.id, "role": role})
