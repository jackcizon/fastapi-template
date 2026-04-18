from fastapi.routing import APIRouter

from src.api.user.routes.avatar import avatar_router
from src.api.user.routes.me import me_router
from src.api.user.routes.password import password_router

user_router = APIRouter()
user_router.include_router(me_router)
user_router.include_router(password_router)
user_router.include_router(avatar_router)
