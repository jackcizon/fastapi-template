from redis.asyncio import Redis
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.rbac.models import User
from src.api.rbac.repos.user_repo import UserRepo
from src.api.user.schemas.password_schema import (
    PasswordResetRequest,
    PasswordResetResponse,
    PasswordForgetRequest,
    PasswordForgetResponse,
)
from src.core.exceptions.auth import AuthError
from src.core.rdb.keys import cache_keys
from src.core.securities.password import Password


class PasswordService:
    @staticmethod
    async def reset(req: PasswordResetRequest, user: User, db: AsyncSession, cache: Redis) -> PasswordResetResponse:
        """use it when jwt refresh token not expired"""
        verification_code_cache = await cache.get(f"{cache_keys.email_verification_code}:{user.email}")
        if verification_code_cache != req["verification_code"]:
            raise AuthError("Verification Error.")

        await UserRepo(db).update(User.id == user.id, {"password": Password.hash(req["new_password"])})
        return PasswordResetResponse(status=True)

    @staticmethod
    async def forget(req: PasswordForgetRequest, db: AsyncSession, cache: Redis) -> PasswordForgetResponse:
        """use it when jwt refresh token expired."""
        verification_code_cache = await cache.get(f"{cache_keys.email_verification_code}:{req['email']}")
        if verification_code_cache != req["verification_code"]:
            raise AuthError("Verification Error.")

        await UserRepo(db).update(User.email == req["email"], {"password": Password.hash(req["new_password"])})
        return PasswordForgetResponse(status=True)
