from typing import Final

from fastapi import status
from sqlalchemy import insert

from src.api.auth.schemas.email_schema import EmailVerificationRequestSchema, EmailVerificationResponseSchema
from src.api.rbac.models import User


class TestEmailVerification:
    url: Final[str] = "/auth/email_verification/"

    async def test_email_verification_success(self, test_client, test_db):
        stat = insert(User).values(name="test_user", email="apitest@example.com", password="123456789")
        await test_db.execute(stat)
        await test_db.flush()

        input_data = EmailVerificationRequestSchema(email="apitest@example.com").model_dump()
        response = await test_client.post(self.url, json=input_data)

        assert response.status_code == status.HTTP_200_OK
        resp = response.json()
        assert len(resp["verification_code"]) == 9

    async def test_login_invalid_password(self, test_client, test_db):
        data = {"email": "notexists@example.com"}
        response = await test_client.post(self.url, json=data)

        assert response.status_code == status.HTTP_401_UNAUTHORIZED
