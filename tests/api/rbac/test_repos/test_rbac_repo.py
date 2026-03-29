from sqlalchemy import Insert, select
from sqlalchemy.dialects.postgresql import insert

from src.api.rbac.models import User, Role, Permission, User2Role
from src.api.rbac.repos.rbac_repo import RbacRepo
from src.api.rbac.repos.role2permission_repo import Role2PermissionRepo


class TestRbacRepo:
    def test_init(self, test_db):
        repo = RbacRepo(test_db)
        assert repo.user
        assert repo.permission
        assert repo.user_role
        assert repo.role_permission

    @staticmethod
    def _insert_user(test_db):
        stat = Insert(User)
        params = {"id": 1, "name": "aafddsfdsa", "password": "isufuhsdiufvds", "email": "cjsjdf@de.com"}
        test_db.execute(stat, params)
        test_db.commit()

    @staticmethod
    def _insert_role_perm(test_db):
        stat = insert(Role)
        params = [{"id": 1, "name": "chairman"}]
        test_db.execute(stat, params)
        test_db.commit()

        stat = Insert(Permission)
        params = {"code": "auth:login"}
        test_db.execute(stat, params)
        test_db.commit()

    @staticmethod
    def _insert_role2perm(test_db):
        role_perm_pairs: list[tuple[str, str]] = [("chairman", "auth:login")]
        repo = Role2PermissionRepo(test_db)

        repo.upsert_by_role_perm_pairs(role_perm_pairs)
        test_db.commit()

    @staticmethod
    def _insert_user2role(test_db, user_id, role_id):
        stat = insert(User2Role)
        params = [{"role_id": role_id, "user_id": user_id}]
        test_db.execute(stat, params)
        test_db.commit()

    @staticmethod
    def _get_user(test_db, id_):
        stat = select(User)
        params = {"id": id_}
        user = test_db.execute(stat, params).scalar_one()
        return user

    def test_get_user_permissions(self, test_db):
        self._insert_user(test_db)
        self._insert_role_perm(test_db)
        self._insert_user2role(test_db, 1, 1)
        self._insert_role2perm(test_db)

        # user_perms = [('rbac:index',), ('auth:me',), ('auth:register',), ('auth:login',)]
        repo = RbacRepo(test_db)

        user = self._get_user(test_db, 1)
        res = repo.get_user_permissions(user)
        print(res)
