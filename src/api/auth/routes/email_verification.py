from fastapi.params import Depends
from fastapi.routing import APIRouter
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.responses import JSONResponse

from src.api.auth.schemas.email_schema import EmailVerificationRequestSchema, EmailVerificationResponseSchema
from src.api.auth.services.email_verification_service import EmailVerificationService
from src.core.db.session import get_db

email_verification_router = APIRouter()


@email_verification_router.post("/email_verification/", name="auth:email_verification:post")
async def email_verification(req: EmailVerificationRequestSchema, db: AsyncSession = Depends(get_db)) -> JSONResponse:
    resp_dict = await EmailVerificationService.verify(request=req.model_dump(), db=db)
    return JSONResponse(content=EmailVerificationResponseSchema(**resp_dict).model_dump())
