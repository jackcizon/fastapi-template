from typing import Final

from fastapi import status
from sqlalchemy import insert

from src.api.auth.schemas.email_schema import EmailVerificationRequestSchema
from src.api.rbac.models import User


class TestEmailVerification:
    url: Final[str] = "/auth/email_verification/"

    @staticmethod
    async def _insert_one_user(test_db):
        stat = insert(User).values(name="test_user", email="apitest@example.com", password="123456789")
        await test_db.execute(stat)
        await test_db.flush()

    async def test_email_verification_success(self, test_client, test_db):
        await self._insert_one_user(test_db)

        input_data = EmailVerificationRequestSchema(email="apitest@example.com", registered=True).model_dump()
        response = await test_client.post(self.url, json=input_data)

        assert response.status_code == status.HTTP_200_OK
        resp = response.json()
        assert len(resp["verification_code"]) == 9

    async def test_email_verification_wrong_email(self, test_client, test_db):
        await self._insert_one_user(test_db)

        input_data = EmailVerificationRequestSchema(email="nonexists@example.com", registered=True).model_dump()
        response = await test_client.post(self.url, json=input_data)

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    async def test_email_verification_rate_limit(self, test_client, test_db):
        await self._insert_one_user(test_db)

        last_status_code = 0
        for i in range(6):
            input_data = EmailVerificationRequestSchema(email="apitest@example.com", registered=True).model_dump()
            response = await test_client.post(self.url, json=input_data)
            last_status_code = response.status_code

        assert last_status_code == 429
