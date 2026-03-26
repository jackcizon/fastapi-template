from fastapi.params import Depends
from fastapi.routing import APIRouter
from sqlalchemy.orm import Session
from starlette.responses import JSONResponse

from src.api.rbac.models import User
from src.api.auth.schemas.login_schema import LoginRequestSchema, LoginResponseSchema
from src.api.auth.services.auth_service import AuthService
from src.core.db.session import get_db
from src.core.securities.jwt import jwt_required_dep

auth_router = APIRouter()


@auth_router.post("/login/", name="auth:login")
async def login(req: LoginRequestSchema, db: Session = Depends(get_db)) -> JSONResponse:
    service = AuthService()
    access, refresh_ = service.login(req=req, db=db)
    schema = LoginResponseSchema(access=access, refresh=refresh_)
    return JSONResponse(content={"access": schema.access, "refresh": schema.refresh})


@auth_router.post("/register/", name="auth:register")
async def register() -> None:
    return None


@auth_router.get("/me/", name="auth:me", openapi_extra={"role": "user"})
async def me(user: User = Depends(jwt_required_dep)) -> JSONResponse:
    """
    personal home page.
    :return:
    """
    return JSONResponse(content={"jwt": "passed", "user_id": user.id})


@auth_router.post("/refresh/", name="auth:refresh")
async def refresh() -> None:
    """todo"""
    return None
