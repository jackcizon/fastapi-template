"""tests for app:demos services"""

from unittest.mock import MagicMock, patch

import pytest
from fastapi import HTTPException

from src.apps.demo.models import Demo
from src.apps.demo.services import DemoService
from src.utils.datastructures import JSONWebToken
from src.apps.demo.schemas import LoginRequestSchema, RegisterRequestSchema


class TestDemoService:
    def test_login_success(self):
        fake_demo = Demo(id=1)

        mock_repo = MagicMock()
        mock_repo.get_demo_by_id.return_value = fake_demo

        service = DemoService(repo=mock_repo)

        req = LoginRequestSchema(id=1)

        # mock token
        with (
            patch.object(JSONWebToken, "create_access_token", return_value="access123"),
            patch.object(JSONWebToken, "create_refresh_token", return_value="refresh123"),
        ):
            demo, access, refresh = service.login(req)

        assert demo is fake_demo
        assert access == "access123"
        assert refresh == "refresh123"

    def test_demo_not_found(self):
        mock_repo = MagicMock()
        mock_repo.get_demo_by_id.return_value = None

        service = DemoService(repo=mock_repo)

        req = LoginRequestSchema(id=2)

        with pytest.raises(HTTPException):
            service.login(req)

    def test_register_demo(self):
        fake_demo = Demo(name="jack")

        mock_repo = MagicMock()
        mock_repo.create_demo.return_value = fake_demo

        service = DemoService(repo=mock_repo)

        req = RegisterRequestSchema(name="jack")
        demo = service.register(req)

        assert demo is fake_demo
        mock_repo.create_demo.assert_called_once_with(name="jack")

    def test_get_demo_by_id(self):
        fake_demo = Demo(id=1)

        mock_repo = MagicMock()
        mock_repo.get_demo_by_id.return_value = fake_demo

        service = DemoService(repo=mock_repo)

        demo = service.get_demo_by_id(1)
        assert demo is fake_demo

    def test_get_demo_info_by_model(self):
        demo = Demo(id=1, name="jack")

        info = DemoService.get_demo_info_by_model(demo)
        assert info["name"] == "jack"
        assert info["id"] == 1

    def test_get_register_success_info(self):
        demo = Demo(id=1)
        info = DemoService.get_register_success_info(demo)
        assert info == {"id": 1, "msg": "register success, please login"}

    def test_get_login_success_info(self):
        demo = Demo(id=1)
        info = DemoService.get_login_success_info(demo, "access", "refresh")
        assert info == {"msg": "success", "id": 1, "access": "access", "refresh": "refresh"}
