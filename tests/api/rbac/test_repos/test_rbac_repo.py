from src.api.rbac.repos.permission_repo import PermissionRepo
from src.api.rbac.repos.rbac_repo import RbacRepo
from src.api.rbac.repos.role2permission_repo import Role2PermissionRepo
from src.api.rbac.repos.role_repo import RoleRepo
from src.api.rbac.repos.user2role_repo import User2RoleRepo
from src.api.rbac.repos.user_repo import UserRepo


class TestRbacRepo:
    user_id = 1
    role_id = 1
    role_name = "123"
    perm_id = 1
    perm_code = "aaa:bbb"

    def test_init(self, test_db):
        repo = RbacRepo(test_db)
        assert repo.user
        assert repo.permission
        assert repo.user_role
        assert repo.role_permission

    async def test_get_user_permissions(self, test_db):
        await UserRepo(test_db).batch_create(
            [{"id": self.user_id, "name": "abcdefg", "email": "qazwsx@qq.com", "password": "123456789"}]
        )
        await RoleRepo(test_db).batch_create([{"id": self.role_id, "name": self.role_name}])
        await User2RoleRepo(test_db).batch_create([{"id": 1, "user_id": self.user_id, "role_id": self.role_id}])
        await PermissionRepo(test_db).batch_create([{"id": self.perm_id, "code": self.perm_code}])
        await Role2PermissionRepo(test_db).batch_create(
            [{"id": 1, "role_id": self.role_id, "permission_id": self.perm_id}]
        )

        user = await UserRepo(test_db).get_one_by_field_eq("id", self.user_id)
        user_perms = await RbacRepo(test_db).get_user_permissions(user)
        assert self.perm_code in user_perms
