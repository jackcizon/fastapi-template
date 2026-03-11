from src.apps.demo.repos import UserRepo


class TestUserRepo:
    def test_create_user(self, db):
        repo = UserRepo(db=db)
        user = repo.create_user(name="user1")
        assert user.id is not None

    def test_get_login_user(self, db):
        repo = UserRepo(db=db)

        user = repo.create_user(name="user2")

        result = repo.get_user_by_id(user.id)

        assert result is not None
        assert result.id == user.id
