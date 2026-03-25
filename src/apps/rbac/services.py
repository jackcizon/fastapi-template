from typing import Sequence, Any

from src.apps.rbac.models import User
from src.apps.rbac.repos import PermissionRepo, Role2PermissionRepo, UserRepo, RbacRepo, RoleRepo


class RoleService:
    def __init__(self, repo: RoleRepo) -> None:
        self.repo = repo

    def batch_create(self, stat: Any = None, params: list = None) -> None:
        self.repo.batch_create(stat, params)


class UserService:
    def __init__(self, repo: UserRepo):
        self.repo = repo

    def get_user_by_id(self, id_: int) -> User | None:
        return self.repo.get_user_by_id(id_)


class PermissionService:
    def __init__(self, repo: PermissionRepo) -> None:
        self.repo = repo

    def del_all(self) -> None:
        self.repo.del_all()

    def upsert_by_codes(self, codes: list[str]) -> None:
        self.repo.upsert_by_codes(codes)

    def del_dirty_data(self, codes: list[str]) -> None:
        self.repo.del_dirty_data(codes)


class Role2PermissionService:
    def __init__(self, repo: Role2PermissionRepo) -> None:
        self.repo = repo

    def del_all(self) -> None:
        self.repo.del_all()

    def upsert_by_list_of_pairs(self, role_perm_pairs: list[tuple[str, str]]) -> None:
        self.repo.upsert_by_role_perm_pairs(role_perm_pairs)

    def del_dirty_data(self, role_perm_pairs: list[tuple[str, str]]) -> None:
        self.repo.del_dirty_data(role_perm_pairs)


class RbacService:
    def __init__(self, repo: RbacRepo):
        self.repo = repo

    def get_user_permissions(self, user: User) -> Sequence:
        return self.repo.get_user_permissions(user)
