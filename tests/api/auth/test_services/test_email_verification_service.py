import pytest
from sqlalchemy.dialects.postgresql import Insert

from src.api.auth.schemas.email_schema import EmailVerificationRequest
from src.api.auth.services.email_verification_service import EmailVerificationService
from src.api.rbac.models import User
from src.core.exceptions.auth import AuthError


class TestEmailVerificationService:
    async def test_verify_success(self, test_db):
        params = [{"name": "test", "email": "email@test.com", "password": "123456789"}]
        stat = Insert(User)
        await test_db.execute(stat, params)
        await test_db.flush()

        req = EmailVerificationRequest(email="email@test.com")
        resp = await EmailVerificationService.verify(req, test_db)
        assert len(resp["verification_code"]) == 9

    async def test_verify_failed(self, test_db):
        user = User(name="test", email="email@test.com", password="12234567")
        test_db.add(user)
        await test_db.flush()

        req = EmailVerificationRequest(email="error_email@qq.com")

        with pytest.raises(AuthError):
            await EmailVerificationService.verify(req, test_db)
