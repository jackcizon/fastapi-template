from typing import Final

from fastapi import status
from sqlalchemy import insert

from src.api.auth.schemas.refresh_schema import RefreshRequestSchema
from src.api.rbac.models import User
from src.utils.datastructures.json_web_token import JSONWebToken


class TestRefresh:
    url: Final[str] = "/auth/refresh/"

    async def test_login_success(self, test_client, test_db):
        user_id = 1

        stat = insert(User).values(id=user_id, name="test_user", email="apitest@example.com", password="123456789")
        await test_db.execute(stat)
        await test_db.flush()

        data = RefreshRequestSchema(refresh=JSONWebToken.create_refresh_token(user_id)).model_dump()
        response = await test_client.post(self.url, json=data)

        assert response.status_code == status.HTTP_200_OK
        resp_json = response.json()
        assert resp_json["access"] is not None

    async def test_refresh_failed(self, test_client, test_db):
        user_id = 1
        wrong_user_id = 2

        stat = insert(User).values(id=user_id, name="test_user", email="apitest@example.com", password="123456789")
        await test_db.execute(stat)
        await test_db.flush()

        data = RefreshRequestSchema(refresh=JSONWebToken.create_access_token(wrong_user_id)).model_dump()
        response = await test_client.post(self.url, json=data)

        assert response.status_code == status.HTTP_401_UNAUTHORIZED
