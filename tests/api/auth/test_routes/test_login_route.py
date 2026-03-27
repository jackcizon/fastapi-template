from typing import Final

from fastapi import status
from sqlalchemy import insert

from src.api.rbac.models import User
from src.core.securities.password import Password


class TestAuthService:
    url: Final[str] = '/auth/login/'

    def test_login_success(self, test_client, test_db):
        raw_password = "secret_password"
        hashed_password = Password.hash(raw_password)

        test_db.execute(
            insert(User).values(
                name="testuser",
                email="api_test@example.com",
                password=hashed_password
            )
        )
        test_db.commit()

        login_data = {
            "email": "api_test@example.com",
            "password": raw_password
        }
        response = test_client.post(self.url, json=login_data)

        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert "access" in data
        assert "refresh" in data
        assert isinstance(data["access"], str)

    def test_login_invalid_password(self, test_client, test_db):
        login_data = {"email": "api_test@example.com", "password": "wrong_password"}
        response = test_client.post(self.url, json=login_data)

        assert response.status_code == status.HTTP_401_UNAUTHORIZED
