"""tests for app:users models"""

from src.apps.users.models import User


def test_user():
    user = User()
    assert user
