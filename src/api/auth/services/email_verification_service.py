from typing import cast

from celery import Task
from redis.asyncio import Redis

from src.api.auth.schemas.email_schema import EmailVerificationRequest, EmailVerificationResponse
from src.core.rdb.keys import cache_keys
from src.core.securities.verification_code import generate_verification_code
from tasks.email.tasks import send_verification_code_email


class EmailVerificationService:
    @staticmethod
    async def verify(
        req: EmailVerificationRequest,
        cache: Redis,
    ) -> EmailVerificationResponse:
        email = req["email"]
        # Login requires, but registration is not.
        # exists = await UserRepo(db).get_one_by_field_eq("email", email)
        # if not exists:
        #     raise AuthError("Email Not Exists.")

        verification_code = generate_verification_code(9)
        await cache.setex(name=f"{cache_keys.email_verification_code}:{email}", time=300, value=verification_code)
        return {"verification_code": verification_code}

    @staticmethod
    async def notify(to_email: str, verification_code: str, subject: str, content: str) -> None:
        cast(Task, send_verification_code_email).delay(to_email, verification_code, subject, content)
