import pytest

from src.api.auth.schemas.register_schema import RegisterRequest
from src.api.auth.services.register_service import RegisterService
from src.api.rbac.repos.role_repo import RoleRepo
from src.api.rbac.repos.user_repo import UserRepo
from src.core.constants import AUTHED_ROLE
from src.core.exceptions.auth import AuthError
from src.core.rdb.keys import cache_keys


class TestRegisterService:
    email = "abcdefg@qq.com"
    verification_code = "qazwsxedc"
    wrong_vcode = "edcwsxqaz"

    async def test_register_success(self, test_db, test_cache):
        await RoleRepo(test_db).batch_create([{"id": 1, "name": AUTHED_ROLE}])

        await test_cache.setex(f"{cache_keys.email_verification_code}:{self.email}", 300, self.verification_code)
        req = RegisterRequest(
            name="abcdefg", email=self.email, password="1233456789", verification_code=self.verification_code
        )
        resp = await RegisterService.register(req, test_db, test_cache)
        assert resp["status"] is True

    async def test_register_failed_email_exists(self, test_db, test_cache):
        await UserRepo(test_db).batch_create(
            [{"id": 1, "name": "aaaaaa", "password": "asffsdfsdfd", "email": self.email}]
        )

        req1 = RegisterRequest(
            name="abcdefg", email=self.email, password="1233456789", verification_code=self.verification_code
        )
        with pytest.raises(AuthError):
            await RegisterService.register(req1, test_db, test_cache)

    async def test_register_failed_wrong_vcode(self, test_db, test_cache):
        await UserRepo(test_db).batch_create(
            [{"id": 1, "name": "aaaaaa", "password": "asffsdfsdfd", "email": self.email}]
        )

        await test_cache.setex(f"{cache_keys.email_verification_code}:{self.email}", 300, self.verification_code)
        req2 = RegisterRequest(
            name="abcdefg", email=self.email, password="1233456789", verification_code=self.wrong_vcode
        )
        with pytest.raises(AuthError):
            await RegisterService.register(req2, test_db, test_cache)
