from typing import Any
from fastapi.params import Depends
from fastapi.routing import APIRouter
from sqlalchemy.orm import Session

from src.apps.demo.repos import DemoRepo
from src.apps.demo.schemas import LoginRequestSchema, RegisterRequestSchema
from src.apps.demo.services import DemoService
from src.utils.auth import get_current_user
from src.core.database import get_db

demos_router = APIRouter()


@demos_router.post("/login/")
async def login(req: LoginRequestSchema, db: Session = Depends(get_db)) -> dict[str, Any]:
    repo = DemoRepo(db=db)
    service = DemoService(repo=repo)
    demo, access, refresh = service.login(req=req)
    login_success_info = service.get_login_success_info(demo, access, refresh)
    return login_success_info


@demos_router.post("/register/")
async def register(req: RegisterRequestSchema, db: Session = Depends(get_db)) -> dict[str, Any]:
    repo = DemoRepo(db=db)
    service = DemoService(repo=repo)
    demo = service.register(req=req)
    register_success_info = service.get_register_success_info(demo)
    return register_success_info


@demos_router.get("/me/")
async def me(
    db: Session = Depends(get_db),
    demo_id: int = Depends(get_current_user),
) -> dict[str, Any]:
    """
    personal home page.
    :param db: db session
    :param demo_id: demo.id(JWT verify)
    :return:
    """
    repo = DemoRepo(db=db)
    service = DemoService(repo=repo)
    demo = service.get_demo_by_id(id_=demo_id)
    demo_info = service.get_demo_info_by_model(demo)
    return demo_info
