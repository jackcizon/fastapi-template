import pytest
from sqlalchemy import Insert

from src.api.rbac.models import User
from src.api.rbac.repos.user_repo import UserRepo
from src.api.user.schemas.password_schema import PasswordResetRequest, PasswordForgetRequest
from src.api.user.services.password_service import PasswordService
from src.core.exceptions.auth import AuthError
from src.core.rdb.keys import cache_keys


class TestPasswordService:
    email = "email@test.com"
    verification_code = "qazwsxedc"
    wrong_verification_code = "wrongcode"

    async def _insert(self, test_db):
        params = [{"name": "test", "email": self.email, "password": "123456789"}]
        stat = Insert(User)
        await test_db.execute(stat, params)
        await test_db.flush()

    async def test_reset_success(self, test_cache, test_db):
        await self._insert(test_db)

        user = await UserRepo(test_db).get_one_by_field_eq("email", self.email)
        await test_cache.setex(f"{cache_keys.email_verification_code}:{self.email}", 300, self.verification_code)

        req = PasswordResetRequest(new_password="123456", verification_code=self.verification_code)
        resp = await PasswordService.reset(req=req, user=user, cache=test_cache, db=test_db)
        assert resp["status"] is True

    async def test_reset_failed(self, test_cache, test_db):
        await self._insert(test_db)

        user = await UserRepo(test_db).get_one_by_field_eq("email", self.email)
        await test_cache.setex(f"{cache_keys.email_verification_code}:{self.email}", 300, self.verification_code)

        req = PasswordResetRequest(new_password="123456", verification_code=self.wrong_verification_code)
        with pytest.raises(AuthError):
            await PasswordService.reset(req=req, user=user, cache=test_cache, db=test_db)

    async def test_forget_success(self, test_cache, test_db):
        await self._insert(test_db)

        await test_cache.setex(f"{cache_keys.email_verification_code}:{self.email}", 300, self.verification_code)

        req = PasswordForgetRequest(new_password="123456", verification_code=self.verification_code, email=self.email)
        resp = await PasswordService.forget(req=req, cache=test_cache, db=test_db)
        assert resp["status"] is True

    async def test_forget_failed(self, test_cache, test_db):
        await self._insert(test_db)

        await test_cache.setex(f"{cache_keys.email_verification_code}:{self.email}", 300, self.verification_code)

        req = PasswordForgetRequest(
            new_password="123456", verification_code=self.wrong_verification_code, email=self.email
        )
        with pytest.raises(AuthError):
            await PasswordService.forget(req=req, cache=test_cache, db=test_db)
