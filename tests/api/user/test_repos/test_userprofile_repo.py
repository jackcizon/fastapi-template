from src.api.user.repos.userprofile_repo import UserProfileRepo


class TestUserProfileRepo:
    def test_init(self, test_db):
        assert UserProfileRepo(test_db)

    async def test_batch_create(self, test_db):
        params = [{"id": 1, "avatar": "null.png"}]
        await UserProfileRepo(test_db).batch_create(params)
