from typing import Sequence

from sqlalchemy import Insert, Select

from src.api.rbac.models import Permission
from src.api.rbac.repos.permission_repo import PermissionRepo


class TestPermissionRepo:
    def test_upsert_by_codes_success(self, test_db):
        repo = PermissionRepo(test_db)
        codes = ["auth:login", "auth:register"]

        repo.upsert_by_codes(codes)

        stat = Select(Permission.code)
        result_codes: Sequence[str] = test_db.execute(stat).scalars().all()

        for code in codes:
            assert code in result_codes

    def test_upsert_by_codes_conflict_do_nothing(self, test_db):
        repo = PermissionRepo(test_db)

        stat = Insert(Permission).values({"code": "auth:login"})
        test_db.execute(stat)
        test_db.commit()

        new_codes = ["auth:login", "auth:logout"]
        repo.upsert_by_codes(new_codes)

        stat = Select(Permission.code)
        result_codes: Sequence[str] = test_db.execute(stat).scalars().all()

        for code in new_codes:
            assert code in result_codes

    def test_del_dirty_data(self, test_db):
        repo = PermissionRepo(test_db)

        old_codes = ["auth:login111111", "auth:register"]
        repo.upsert_by_codes(old_codes)

        new_codes = ["auth:login", "auth:register"]
        repo.upsert_by_codes(new_codes)
        repo.del_dirty_data(new_codes)

        stat = Select(Permission.code)
        result_codes: Sequence[str] = test_db.execute(stat).scalars().all()

        for code in new_codes:
            assert code in result_codes
