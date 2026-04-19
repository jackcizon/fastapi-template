from src.api.rbac.repos.user2role_repo import User2RoleRepo


class TestUser2RoleRepo:
    def test_init(self, test_db):
        assert User2RoleRepo(test_db)

    async def test_batch_create(self, test_db):
        params = [{"id": 1, "user_id": 1, "role_id": 1}]
        await User2RoleRepo(test_db).batch_create(params)
