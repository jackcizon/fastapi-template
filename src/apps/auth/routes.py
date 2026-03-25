from typing import Any
from fastapi.params import Depends
from fastapi.routing import APIRouter
from sqlalchemy.orm import Session
from starlette.responses import JSONResponse

from src.apps.auth.schemas import LoginRequestSchema, LoginResponseSchema, RegisterRequestSchema
from src.apps.rbac.models import User
from src.utils.dependencies.auth import jwt_required_dep
from src.core.database import get_db
from src.apps.auth.services import AuthService

auth_router = APIRouter()


@auth_router.post("/login/", name="auth:login")
async def login(req: LoginRequestSchema, db: Session = Depends(get_db)) -> JSONResponse:
    service = AuthService()
    access, refresh_ = service.login(req=req, db=db)
    schema = LoginResponseSchema(access=access, refresh=refresh_)
    return JSONResponse(content={"access": schema.access, "refresh": schema.refresh})


@auth_router.post("/register/", name="auth:register")
async def register(req: RegisterRequestSchema, db: Session = Depends(get_db)) -> Any:
    #     repo = DemoRepo(db=db)
    #     service = DemoService(repo=repo)
    #     demo = service.register(req=req)
    #     register_success_info = service.get_register_success_info(demo)
    #     return register_success_info
    pass


@auth_router.get("/me/", name="auth:me", openapi_extra={"role": "user"})
async def me(user: User = Depends(jwt_required_dep)) -> JSONResponse:
    """
    personal home page.
    :return:
    """
    return JSONResponse(content={"jwt": "passed", "user_id": user.id})


async def refresh() -> None:
    """todo"""
    return None
