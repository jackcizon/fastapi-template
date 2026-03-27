from fastapi import APIRouter

register_router = APIRouter()


@register_router.post("/register/", name="auth:register")
async def register() -> None:
    return None
