from src.apps.users.repos import UserRepo


class TestUserRepo:
    def test_create_user(self, db):
        repo = UserRepo(db=db)

        user = repo.create_user(gender=1, nick_name="jack")

        assert user.id is not None
        assert user.nick_name == "jack"
        assert user.gender == 1
        assert user.open_id is not None

    def test_get_login_user(self, db):
        repo = UserRepo(db=db)

        user = repo.create_user(gender=1, nick_name="jack")

        result = repo.get_login_user(user.open_id)

        assert result is not None
        assert result.open_id == user.open_id
