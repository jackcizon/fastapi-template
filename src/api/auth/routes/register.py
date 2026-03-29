from fastapi import APIRouter

register_router = APIRouter()


@register_router.post("/register/", name="auth:register")  # pragma: no cover
async def register() -> None:
    return None
