from fastapi.routing import APIRouter

from src.apps.users.repos import UserRepo
from src.apps.users.services import UserService

users_router = APIRouter()


@users_router.get("/")
async def users() -> dict:
    return UserService(repo=UserRepo()).list()
