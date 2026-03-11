"""tests for app:users services"""

from unittest.mock import MagicMock, patch

import pytest
from fastapi import HTTPException

from src.apps.users.models import User
from src.apps.users.services import UserService
from src.utils.datastructures import JSONWebToken
from src.apps.users.schemas import LoginRequestSchema, RegisterRequestSchema


class TestUserService:
    def test_login_success(self):
        fake_user = User(id=1)

        mock_repo = MagicMock()
        mock_repo.get_login_user.return_value = fake_user

        service = UserService(repo=mock_repo)

        req = LoginRequestSchema(id=1)

        # mock token
        with (
            patch.object(JSONWebToken, "create_access_token", return_value="access123"),
            patch.object(JSONWebToken, "create_refresh_token", return_value="refresh123"),
        ):
            user, access, refresh = service.login(req)

        assert user is fake_user
        assert access == "access123"
        assert refresh == "refresh123"

    def test_login_user_not_found(self):
        mock_repo = MagicMock()
        mock_repo.get_login_user.return_value = None

        service = UserService(repo=mock_repo)

        req = LoginRequestSchema(open_id="abc123")

        with pytest.raises(HTTPException):
            service.login(req)

    def test_register_user(self):
        fake_user = User(id=1, name="jack")

        mock_repo = MagicMock()
        mock_repo.create_user.return_value = fake_user

        service = UserService(repo=mock_repo)

        req = RegisterRequestSchema(nick_name="jack")
        user = service.register(req)

        assert user is fake_user
        mock_repo.create_user.assert_called_once_with(name="jack")

    def test_get_user_by_open_id(self):
        fake_user = User(id=1)

        mock_repo = MagicMock()
        mock_repo.get_login_user.return_value = fake_user

        service = UserService(repo=mock_repo)

        user = service.get_user_by_id(1)
        assert user is fake_user

    def test_get_user_info_by_model(self):
        user = User(id=1, name="jack")

        info = UserService.get_user_info_by_model(user)
        assert info["name"] == "jack"
        assert info["id"] == 1

    def test_get_register_success_info(self):
        user = User(id=1)
        info = UserService.get_register_success_info(user)
        assert info == {"id": 1, "msg": "register success, please login"}

    def test_get_login_success_info(self):
        user = User(id=1)
        info = UserService.get_login_success_info(user, "access", "refresh")
        assert info == {"msg": "success", "id": 1, "access": "access", "refresh": "refresh"}
