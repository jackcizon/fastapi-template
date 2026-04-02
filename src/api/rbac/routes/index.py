from fastapi import APIRouter
from fastapi.params import Depends
from starlette.responses import JSONResponse

from src.api.rbac.models import User
from src.core.constants import ROLE
from src.core.securities.rbac import role_permission_check_dep

index_router = APIRouter()


@index_router.get("/index/", name="rbac:index:get", openapi_extra={"role": ROLE.STAFF.value})
async def rbac_index(
    user_role: tuple[User, str] = Depends(role_permission_check_dep),
) -> JSONResponse:  # pragma: no cover
    user, role = user_role
    return JSONResponse(content={"user": user.id, "role": role})
