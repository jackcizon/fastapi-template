import pytest

from src.api.auth.schemas.login_schema import LoginRequestSchema
from src.api.auth.services.login_service import LoginService
from src.api.rbac.models import User
from src.core.exceptions.auth import AuthError
from src.core.securities.password import Password


class TestLoginService:
    def test_login_success(self, test_db):
        raw_password = "secure_password123"
        hashed_password = Password.hash(raw_password)

        user = User(name="test", email="login@test.com", password=hashed_password)
        test_db.add(user)
        test_db.commit()

        req = LoginRequestSchema(email="login@test.com", password=raw_password)
        resp_schema = LoginService.login(req, test_db)

        assert isinstance(resp_schema.access, str)
        assert isinstance(resp_schema.refresh, str)

    def test_login_failed_wrong_password(self, test_db):
        hashed = Password.hash("correct_password")
        user = User(name="test", email="wrong_pwd@test.com", password=hashed)
        test_db.add(user)
        test_db.commit()

        req = LoginRequestSchema(email="wrong_pwd@test.com", password="bad_password")

        with pytest.raises(AuthError):
            LoginService.login(req, test_db)

    def test_login_failed_user_not_found(self, test_db):
        req = LoginRequestSchema(email="nobody@test.com", password="any_password")

        with pytest.raises(AuthError):
            LoginService.login(req, test_db)
