from typing import Any

from fastapi.params import Depends
from fastapi.routing import APIRouter
from redis.asyncio import Redis
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.responses import JSONResponse

from src.api.auth.schemas.email_schema import EmailVerificationRequestSchema, EmailVerificationResponseSchema
from src.api.auth.services.email_verification_service import EmailVerificationService
from src.core.db.session import get_db
from src.core.rdb.base import get_cache
from src.core.securities.ratelimit.deps import RateLimitDep

email_verification_router = APIRouter()


@email_verification_router.post("/email_verification/", name="auth:email_verification:post")
async def email_verification(
    req: EmailVerificationRequestSchema,
    cache: Redis = Depends(get_cache),
    db: AsyncSession = Depends(get_db),
    _: Any = Depends(RateLimitDep(1, 60)),
) -> JSONResponse:
    resp_dict = await EmailVerificationService.verify(req=req.model_dump(), cache=cache, db=db)
    # await EmailVerificationService.notify(
    #     to_email=req.email,
    #     verification_code=resp_dict["verification_code"],
    #     subject="Email Verification",
    #     content="Email Verification"
    # )
    return JSONResponse(content=EmailVerificationResponseSchema(**resp_dict).model_dump())
