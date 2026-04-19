from src.api.rbac.repos.role2permission_repo import Role2PermissionRepo


class TestRole2PermissionRepo:
    def test_init(self, test_db):
        assert Role2PermissionRepo(test_db) is not None
