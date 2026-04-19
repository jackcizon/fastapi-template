from src.api.rbac.repos.permission_repo import PermissionRepo


class TestPermissionRepo:
    def test_init(self, test_db):
        assert PermissionRepo(test_db)
