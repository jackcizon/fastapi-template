from typing import Any
from fastapi.params import Depends
from fastapi.routing import APIRouter
from sqlalchemy.orm import Session

from src.apps.demo.repos import UserRepo
from src.apps.demo.schemas import LoginRequestSchema, RegisterRequestSchema
from src.apps.demo.services import UserService
from src.utils.auth import get_current_user
from src.core.database import get_db

users_router = APIRouter()


@users_router.post("/login/")
async def login(req: LoginRequestSchema, db: Session = Depends(get_db)) -> dict[str, Any]:
    repo = UserRepo(db=db)
    service = UserService(repo=repo)
    user, access, refresh = service.login(req=req)
    login_success_info = service.get_login_success_info(user, access, refresh)
    return login_success_info


@users_router.post("/register/")
async def register(req: RegisterRequestSchema, db: Session = Depends(get_db)) -> dict[str, Any]:
    repo = UserRepo(db=db)
    service = UserService(repo=repo)
    user = service.register(req=req)
    register_success_info = service.get_register_success_info(user)
    return register_success_info


@users_router.get("/me/")
async def me(
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user),
) -> dict[str, Any]:
    """
    personal home page.
    :param db: db session
    :param user_id: user.id(JWT verify)
    :return:
    """
    repo = UserRepo(db=db)
    service = UserService(repo=repo)
    user = service.get_user_by_id(id_=user_id)
    user_info = service.get_user_info_by_model(user)
    return user_info
