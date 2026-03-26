from fastapi import APIRouter
from fastapi.params import Depends
from starlette.responses import JSONResponse

from src.api.rbac.models import User
from src.core.securities.rbac import role_permission_check_dep

rbac_router = APIRouter()


@rbac_router.get("/index/", name="rbac:index", openapi_extra={"role": "staff"})
def rbac_index(user_role: tuple[User, str] = Depends(role_permission_check_dep)) -> JSONResponse:
    user, role = user_role
    return JSONResponse(content={"user": user.id, "role": role})
