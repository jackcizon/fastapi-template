from typing import Any
from datetime import datetime

from faker import Faker
from click import Context, Parameter, Option, Command

from src.api.rbac.repos.user_repo import UserRepo
from src.core.db.session import SessionLocal
from src.core.securities.password import Password


class BatchCreateFakeUsersCommand(Command):
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self._dict = {"opt": {"number": ["-n", "--number"]}, "arg": {"demo-arg": ["demo-arg"]}}
        self.params: list[Parameter] = [
            Option(param_decls=self._dict["opt"]["number"], default=10, type=int),
        ]
        self.help = "default password is `123456`, they don't have roles, they are login visitors."

    def invoke(self, ctx: Context) -> Any:
        number = int(ctx.params.get("number"))
        number = 100_000 if number > 100_000 else number
        self._batch_create(number)
        return super().invoke(ctx)

    @staticmethod
    def _batch_create(num: int) -> None:
        faker_ = Faker()
        params = []

        # speed up
        # calculate one time, only in batch-create-users
        hashed_password = Password.hash("123456")
        # same datetime
        date_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")

        for _ in range(num):
            params.append(
                {
                    "name": faker_.name()[0:15],
                    "email": faker_.email()[0:31],
                    "password": hashed_password,
                    "created_time": date_time,
                    "is_deleted": False,
                }
            )

        with SessionLocal() as db:
            try:
                UserRepo(db).batch_create(params=params)
                db.commit()
            except Exception as e:
                print(e)
                db.rollback()
                raise
