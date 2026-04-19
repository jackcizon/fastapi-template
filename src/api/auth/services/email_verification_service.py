from typing import cast

from celery import Task
from redis.asyncio import Redis
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.auth.schemas.email_schema import EmailVerificationRequest, EmailVerificationResponse
from src.api.rbac.repos.user_repo import UserRepo
from src.core.exceptions.auth import AuthError
from src.core.rdb.keys import cache_keys
from src.core.securities.verification_code import generate_verification_code
from tasks.email.tasks import send_verification_code_email


class EmailVerificationService:
    @staticmethod
    async def verify(req: EmailVerificationRequest, cache: Redis, db: AsyncSession) -> EmailVerificationResponse:
        email = req["email"]
        exists = await UserRepo(db).get_one_by_field_eq("email", email)
        if req["registered"] is True:
            if not exists:
                raise AuthError("Email not Exists.")
        if req["registered"] is False:
            if exists:
                raise AuthError("Email Exists.")

        verification_code = generate_verification_code(9)
        await cache.setex(name=f"{cache_keys.email_verification_code}:{email}", time=300, value=verification_code)
        return EmailVerificationResponse(verification_code=verification_code)

    @staticmethod
    async def notify(to_email: str, verification_code: str, subject: str, content: str) -> None:  # pragma: no cover
        cast(Task, send_verification_code_email).delay(to_email, verification_code, subject, content)
