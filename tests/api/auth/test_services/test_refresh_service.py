from unittest.mock import patch

import pytest

from src.api.rbac.models import User
from src.api.auth.schemas.refresh_schema import RefreshRequestSchema
from src.api.auth.services.refresh_service import RefreshService
from src.core.exceptions.auth import AuthError
from src.core.exceptions.jwt import JWTError


class TestRefreshService:
    @patch("src.api.auth.services.refresh_service.JSONWebToken")
    def test_refresh_success_with_sqlite(self, mock_jwt, test_db):
        """
        @patch("src.utils.datastructures.json_web_token.JSONWebToken")  # error
        @patch("src.api.auth.services.refresh_service.JSONWebToken")  # right

        in src.api.auth.services.refresh_service:
        `RefreshService` invokes `src.utils.datastructures.json_web_token.JSONWebToken`
        `from src.utils.datastructures.json_web_token import JSONWebToken`

        patch path:
        `src.api.auth.services.refresh_service.JSONWebToken`
        """
        test_user = User(id=1, name="test_user", email='test_email@qq.com', password='123456')
        test_db.add(test_user)
        test_db.commit()

        mock_jwt.decode_token.return_value = {"user_id": 1}
        mock_jwt.create_access_token.return_value = "new_access_token_123"

        req = RefreshRequestSchema(refresh="valid_refresh_token")
        response = RefreshService.refresh(req, test_db)

        assert response.access == "new_access_token_123"

    @patch("src.api.auth.services.refresh_service.JSONWebToken")
    def test_refresh_user_not_found_in_sqlite(self, mock_jwt, test_db):
        mock_jwt.decode_token.return_value = {"user_id": 99}

        req = RefreshRequestSchema(refresh="token_for_non_existent_user")

        with pytest.raises(AuthError):
            RefreshService.refresh(req, test_db)
