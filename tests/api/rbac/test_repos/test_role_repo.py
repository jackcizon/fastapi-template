from faker import Faker
from sqlalchemy import Select, func, delete

from src.api.rbac.models import Role
from src.api.rbac.repos.role_repo import RoleRepo


class TestRoleRepo:
    async def test_batch_create(self, test_db):
        stat = delete(Role)
        await test_db.execute(stat)
        await test_db.flush()

        faker_ = Faker()
        num = 10
        params = []

        for _ in range(num):
            params.append({"name": faker_.name()[0:10]})

        await RoleRepo(test_db).batch_create(params=params)
        await test_db.flush()

        stat = Select(func.count()).select_from(Role)
        res = await test_db.execute(stat)
        count = res.scalar()

        assert count == num
