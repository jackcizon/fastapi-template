from fastapi import APIRouter

refresh_router = APIRouter()


@refresh_router.post("/refresh/", name="auth:refresh")
async def refresh() -> None:
    return None
