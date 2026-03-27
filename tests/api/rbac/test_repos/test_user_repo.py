from datetime import datetime
from typing import Any

from faker import Faker
from sqlalchemy import Select, func, delete

from src.api.rbac.models import User
from src.api.rbac.repos.user_repo import UserRepo


class TestUserRepo:
    def test_get_user_by_email(self, test_db):
        name = "abcdefg"
        email = "aaa@qq.com"
        password = "123456"
        user = User(name=name, email=email, password=password)
        test_db.add(user)
        test_db.commit()

        user_dict: dict[str, Any] | None = UserRepo(test_db).get_user_by_email(email)

        assert user_dict.get("id") is not None
        assert user_dict.get("name") == name
        assert user_dict.get("email") == email
        assert user_dict.get("password") == password

    def test_batch_create(self, test_db):
        stat = delete(User)
        test_db.execute(stat)
        test_db.commit()

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

        UserRepo(test_db).batch_create(params=params)
        test_db.commit()

        stat = Select(func.count()).select_from(User)
        count = test_db.execute(stat).scalar()

        assert count == num
