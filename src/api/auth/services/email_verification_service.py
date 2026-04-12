from random import randint

from sqlalchemy.ext.asyncio import AsyncSession

from src.api.auth.schemas.email_schema import EmailVerificationRequest, EmailVerificationResponse
from src.api.rbac.repos.user_repo import UserRepo
from src.core.exceptions.auth import AuthError


class EmailVerificationService:
    @staticmethod
    async def verify(request: EmailVerificationRequest, db: AsyncSession) -> EmailVerificationResponse:
        """TODO: 客户端限流,ip限流"""
        verification_code = str(randint(100_000_000, 999_999_999))
        exists = await UserRepo(db).get_one_by_field_eq("email", request["email"])
        if not exists:
            raise AuthError("Email Not Exists.")
        return {"verification_code": verification_code}
