from typing import Any
from fastapi.params import Depends
from fastapi.routing import APIRouter
from sqlalchemy.orm import Session

from src.apps.auth.repos import DemoRepo
from src.apps.auth.schemas import LoginRequestSchema, RegisterRequestSchema
from src.apps.auth.services import DemoService
from src.utils.auth import get_current_user
from src.core.database import get_db

auth_router = APIRouter()


@auth_router.post("/login/", name='auth:login')
async def login(req: LoginRequestSchema, db: Session = Depends(get_db)) -> dict[str, Any]:
    repo = DemoRepo(db=db)
    service = DemoService(repo=repo)
    demo, access, refresh = service.login(req=req)
    login_success_info = service.get_login_success_info(demo, access, refresh)
    return login_success_info


@auth_router.post("/register/", name="auth:register")
async def register(req: RegisterRequestSchema, db: Session = Depends(get_db)) -> dict[str, Any]:
    repo = DemoRepo(db=db)
    service = DemoService(repo=repo)
    demo = service.register(req=req)
    register_success_info = service.get_register_success_info(demo)
    return register_success_info


@auth_router.get("/me/", name="auth:me")
async def me(
        db: Session = Depends(get_db),
        demo_id: int = Depends(get_current_user),
) -> dict[str, Any]:
    """
    personal home page.
    :param db: db session
    :param demo_id: auth.id(JWT verify)
    :return:
    """
    repo = DemoRepo(db=db)
    service = DemoService(repo=repo)
    demo = service.get_demo_by_id(id_=demo_id)
    demo_info = service.get_demo_info_by_model(demo)
    return demo_info

# for route in auth_router.routes:
#     print(route.name)