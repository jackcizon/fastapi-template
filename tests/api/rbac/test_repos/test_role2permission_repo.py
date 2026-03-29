from sqlalchemy import Select
from sqlalchemy.dialects.postgresql import Insert

from src.api.rbac.models import Role2Permission, Role, Permission
from src.api.rbac.repos.role2permission_repo import Role2PermissionRepo


class TestRole2PermissionRepo:
    """
    Why I use hard code `id=1` in this test is perfect.

    1. Instead of using a development database, I use a dedicated Postgres container(Test Server).
    2. SAVEPOINT Transaction rollback, each function is isolated.
    3. Hard-coded IDs are a contract in my test code: I define: User_id is always 1, Role_id is always 1.
    """

    @staticmethod
    def _insert_roles_and_perms(test_db):
        stat = Insert(Role)
        params = [{"name": "chairman"}, {"name": "ceo"}, {"name": "cto"}]
        stat = stat.on_conflict_do_nothing(index_elements=["name"])
        test_db.execute(stat, params)
        test_db.commit()

        stat = Insert(Permission)
        params = {"code": "auth:login"}
        test_db.execute(stat, params)
        test_db.commit()

    @staticmethod
    def _upsert(test_db):
        role_perm_pairs: list[tuple[str, str]] = [
            ("chairman", "auth:login"),
            ("ceo", "auth:login"),
            ("cto", "auth:login"),
        ]
        repo = Role2PermissionRepo(test_db)

        repo.upsert_by_role_perm_pairs(role_perm_pairs)
        test_db.commit()

        modified_role_perm_pairs_test_on_conflict = [("chairman", "auth:login")]
        repo.upsert_by_role_perm_pairs(modified_role_perm_pairs_test_on_conflict)
        test_db.commit()

    def test_upsert_role_perm_pairs(self, test_db):
        self._insert_roles_and_perms(test_db)
        self._upsert(test_db)

        stat = Select(Role2Permission.role_id, Role2Permission.permission_id)
        res = test_db.execute(stat).mappings().all()
        assert res is not None

    def test_del_dirty_data(self, test_db):
        self._insert_roles_and_perms(test_db)
        self._upsert(test_db)

        # dirty data
        role_perm_pairs: list[tuple[str, str]] = [
            ("chairman", "auth:login111111111"),
            ("ceo", "auth:login"),
            ("cto", "auth:login"),
        ]
        repo = Role2PermissionRepo(test_db)

        repo.upsert_by_role_perm_pairs(role_perm_pairs)
        test_db.commit()

        role_perm_pairs: list[tuple[str, str]] = [
            ("chairman", "auth:login"),
            ("ceo", "auth:login"),
            ("cto", "auth:login"),
        ]
        repo = Role2PermissionRepo(test_db)

        repo.upsert_by_role_perm_pairs(role_perm_pairs)
        test_db.commit()

        repo.del_dirty_data(role_perm_pairs)
        test_db.commit()
