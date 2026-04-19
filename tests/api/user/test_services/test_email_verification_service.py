import pytest
from sqlalchemy import Insert

from src.api.auth.schemas.email_schema import EmailVerificationRequest
from src.api.auth.services.email_verification_service import EmailVerificationService
from src.api.rbac.models import User
from src.core.exceptions.auth import AuthError


class TestEmailVerificationService:
    email = "email@test.com"
    wrong_email = "wrongemail@aa.com"

    async def _insert(self, test_db):
        params = [{"name": "test", "email": self.email, "password": "123456789"}]
        stat = Insert(User)
        await test_db.execute(stat, params)
        await test_db.flush()

    async def test_verify_success(self, test_cache, test_db):
        await self._insert(test_db)

        req = EmailVerificationRequest(email=self.email, registered=True)
        resp = await EmailVerificationService.verify(req, test_cache, test_db)
        assert len(resp["verification_code"]) == 9

    async def test_verify_failed_email_not_exists(self, test_cache, test_db):
        await self._insert(test_db)

        req1 = EmailVerificationRequest(email=self.wrong_email, registered=True)
        with pytest.raises(AuthError):
            await EmailVerificationService.verify(req1, test_cache, test_db)

    async def test_verify_failed_email_exists(self, test_cache, test_db):
        await self._insert(test_db)

        req2 = EmailVerificationRequest(email=self.email, registered=False)
        with pytest.raises(AuthError):
            await EmailVerificationService.verify(req2, test_cache, test_db)
