from typing import Any

from fastapi import APIRouter
from fastapi.params import Depends
from redis.asyncio import Redis
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.responses import JSONResponse

from src.api.auth.schemas.register_schema import RegisterRequestSchema, RegisterResponseSchema
from src.api.auth.services.register_service import RegisterService
from src.core.db.session import get_db
from src.core.rdb.base import get_cache
from src.core.securities.ratelimit.deps import RateLimitDep

register_router = APIRouter()


@register_router.post("/register/", name="auth:register:post")
async def register(
    req: RegisterRequestSchema,
    db: AsyncSession = Depends(get_db),
    cache: Redis = Depends(get_cache),
    _: Any = Depends(RateLimitDep(5, 60)),
) -> JSONResponse:
    """
    ```
    step 1:
    post `/auth/email_verification/`, get `verification_code`

    step 2:
    post /auth/register/`
    ```
    """
    resp_dict = await RegisterService.register(req.model_dump(), db, cache)
    return JSONResponse(content=RegisterResponseSchema(**resp_dict).model_dump())
