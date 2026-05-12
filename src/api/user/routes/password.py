from fastapi import APIRouter, Depends
from redis.asyncio import Redis
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.responses import JSONResponse

from src.api.rbac.models import User
from src.api.user.schemas.password_schema import (
    PasswordResetRequestSchema,
    PasswordForgetRequestSchema,
    PasswordResetResponseSchema,
)
from src.api.user.services.password_service import PasswordService
from src.core.db.session import get_db
from src.core.cache.base import get_cache
from src.core.securities.jwt import jwt_required_dep

password_router = APIRouter()


@password_router.post("/password/reset/", name="user:password_reset:post")
async def password_reset(
    req: PasswordResetRequestSchema,
    user: User = Depends(jwt_required_dep),
    db: AsyncSession = Depends(get_db),
    cache: Redis = Depends(get_cache),
) -> JSONResponse:
    """
    ```
    step 1:
    post `/auth/email_verification/`, get `verification_code`

    step2:
    post `/user/password/reset/`
    ```
    """
    resp_dict = await PasswordService.reset(req.model_dump(), user, db, cache)
    return JSONResponse(PasswordResetResponseSchema(**resp_dict).model_dump())


@password_router.post("/password/forget/", name="user:password_forget:post")
async def password_forget(
    req: PasswordForgetRequestSchema, db: AsyncSession = Depends(get_db), cache: Redis = Depends(get_cache)
) -> JSONResponse:
    """
    ```
    step 1:
    post `/auth/email_verification/`, get `verification_code`

    step 2:
    post `/user/password/forget/`
    ```
    """
    resp_dict = await PasswordService.forget(req.model_dump(), db, cache)
    return JSONResponse(content=PasswordResetResponseSchema(**resp_dict).model_dump())
