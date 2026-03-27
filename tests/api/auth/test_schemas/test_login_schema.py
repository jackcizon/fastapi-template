import pytest
from pydantic import ValidationError

from src.api.auth.schemas.login_schema import LoginRequestSchema


class TestLoginSchema:
    def test_login_request_valid(self):
        data = {"email": "abc123@qq.com", "password": "password123"}
        user = LoginRequestSchema(**data)
        assert user.email == data["email"]

    @pytest.mark.parametrize(
        "invalid_email",
        [
            "short",
            "0abc@test.com",
            "@example.com",
            "abc@com",
            "abc.test.com",
            " a@b.com",
        ],
    )
    def test_login_request_email_pattern_invalid(self, invalid_email):
        with pytest.raises(ValidationError) as exc:
            LoginRequestSchema(email=invalid_email, password="valid_password")

        assert "email" in str(exc.value)

    def test_login_request_password_too_short(self):
        with pytest.raises(ValidationError):
            LoginRequestSchema(email="valid@test.com", password="123")

    def test_login_request_password_too_long(self):
        with pytest.raises(ValidationError):
            LoginRequestSchema(email="valid@test.com", password="a" * 33)
