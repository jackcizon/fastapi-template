from datetime import datetime

from faker import Faker
from sqlalchemy import Select, func, delete
from sqlalchemy.dialects.postgresql import Insert

from src.api.rbac.models import User
from src.api.rbac.repos.user_repo import UserRepo


class TestUserRepo:
    async def test_get_user_by_email(self, test_db):
        name = "abcdefg"
        email = "aaa@qq.com"
        password = "123456"
        stat = Insert(User)
        params = [{"name": name, "email": email, "password": password}]
        await test_db.execute(stat, params)
        await test_db.flush()

        user: User | None = await UserRepo(test_db).get_one_by_field_eq("email", email)

        assert user.id is not None
        assert user.name == name
        assert user.email == email
        assert user.password == password

    async def test_batch_create(self, test_db):
        stat = delete(User)
        await test_db.execute(stat)
        await test_db.flush()

        faker_ = Faker()
        num = 10
        params = []

        password = "123456"
        date_time = datetime.now()

        for _ in range(num):
            params.append(
                {
                    "name": faker_.name()[0:15],
                    "email": faker_.email()[0:31],
                    "password": password,
                    "created_time": date_time,
                    "is_deleted": False,
                }
            )

        await UserRepo(test_db).batch_create(params=params)
        await test_db.flush()

        stat = Select(func.count()).select_from(User)
        res = await test_db.execute(stat)
        count = res.scalar()

        assert count == num
