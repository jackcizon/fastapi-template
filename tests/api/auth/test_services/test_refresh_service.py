from unittest.mock import patch

import pytest
from sqlalchemy.dialects.postgresql import insert

from src.api.rbac.models import User
from src.api.auth.schemas.refresh_schema import RefreshRequest
from src.api.auth.services.refresh_service import RefreshService
from src.core.exceptions.auth import AuthError


class TestRefreshService:
    @patch("src.api.auth.services.refresh_service.JSONWebToken")
    async def test_refresh_success(self, mock_jwt, test_db):
        """
        @patch("src.utils.datastructures.json_web_token.JSONWebToken")  # error
        @patch("src.api.auth.services.refresh_service.JSONWebToken")  # right

        in src.api.auth.services.refresh_service:
        `RefreshService` invokes `src.utils.datastructures.json_web_token.JSONWebToken`
        `from src.utils.datastructures.json_web_token import JSONWebToken`

        patch path:
        `src.api.auth.services.refresh_service.JSONWebToken`
        """
        stat = insert(User)
        params = [{"id": 1, "name": "test_user", "email": "test_email@qq.com", "password": "123456"}]
        await test_db.execute(stat, params)
        await test_db.commit()

        mock_jwt.decode_token.return_value = {"user_id": 1}
        mock_jwt.create_access_token.return_value = "new_access_token_123"

        req = RefreshRequest(refresh="valid_refresh_token")
        response = await RefreshService.refresh(req, test_db)

        assert response["access"] == "new_access_token_123"

    @patch("src.api.auth.services.refresh_service.JSONWebToken")
    async def test_refresh_user_not_found(self, mock_jwt, test_db):
        mock_jwt.decode_token.return_value = {"user_id": 99}

        req = RefreshRequest(refresh="token_for_non_existent_user")

        with pytest.raises(AuthError):
            await RefreshService.refresh(req, test_db)
