from datetime import datetime
from typing import Any

from faker import Faker
from sqlalchemy import Select, func, delete

from src.api.rbac.models import User, Role
from src.api.rbac.repos.role_repo import RoleRepo
from src.api.rbac.repos.user_repo import UserRepo


class TestRoleRepo:
    def test_batch_create(self, test_db):
        stat = delete(Role)
        test_db.execute(stat)
        test_db.commit()

        faker_ = Faker()
        num = 10
        params = []

        for _ in range(num):
            params.append({"name": faker_.name()[0:10]})

        RoleRepo(test_db).batch_create(params=params)
        test_db.commit()

        stat = Select(func.count()).select_from(Role)
        count = test_db.execute(stat).scalar()

        assert count == num
