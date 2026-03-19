from src.apps.rbac.repos import PermissionRepo, Role2PermissionRepo


class PermissionService:
    def __init__(self, repo: PermissionRepo) -> None:
        self.repo = repo

    def del_all(self):
        self.repo.del_all()

    def upsert_by_codes(self, codes: list[str]) -> None:
        self.repo.upsert_by_codes(codes)

    def del_dirty_data(self, codes: list[str]):
        self.repo.del_dirty_data(codes)


class Role2PermissionService:
    def __init__(self, repo: Role2PermissionRepo) -> None:
        self.repo = repo

    def del_all(self):
        self.repo.del_all()

    def upsert_by_list_of_pairs(self, role_perm_pairs: list[tuple[str, str]]) -> None:
        self.repo.upsert_by_role_perm_pairs(role_perm_pairs)

    def del_dirty_data(self, role_perm_pairs: list[tuple[str, str]]):
        self.repo.del_dirty_data(role_perm_pairs)
