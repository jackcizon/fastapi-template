"""tests for app:users services"""

from src.apps.users.repos import UserRepo
from src.apps.users.services import UserService


def test_list_users():
    service = UserService(repo=UserRepo())
    users = service.list()
    assert len(users) == 2
