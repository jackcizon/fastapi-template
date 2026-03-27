import os
from typing import Any

from click import Context, Command, Parameter, Option

from src.core.config import SRC_DIR, ROOT_DIR


class CreateApiCommand(Command):
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)

        self._dict = {"opt": {"name": ["-n", "--name"]}, "arg": {}}
        self.params: list[Parameter] = [
            Option(param_decls=self._dict.get("opt").get("name"), type=str),
        ]

    def invoke(self, ctx: Context) -> Any:
        name = ctx.params.get("name")
        try:
            self._create_api(name)
            self._create_api_tests(name)
        except Exception as e:
            print(e)
            raise
        finally:
            return super().invoke(ctx)

    @staticmethod
    def _create_api(name: str) -> None:
        print(f"try creating api:{name}....")
        target_dir = os.path.join(SRC_DIR, "api")
        os.chdir(target_dir)
        os.mkdir(name)
        api_dir = os.path.join(target_dir, name)
        os.chdir(api_dir)

        files = ("__init__.py", "router.py", "models.py")
        for file in files:
            fd = os.open(file, os.O_CREAT)
            os.close(fd)

        dirs = ("commands", "services", "repos", "schemas", "routes")
        for dir_ in dirs:
            os.mkdir(dir_)
            fd = os.open(f"{dir_}/__init__.py", os.O_CREAT)
            os.close(fd)

        print(f"api {name} created.")

    @staticmethod
    def _create_api_tests(name: str) -> None:
        print(f"try creating tests:{name}....")

        target_dir = os.path.join(ROOT_DIR, "tests/api")
        os.chdir(target_dir)
        os.mkdir(name)
        api_dir = os.path.join(target_dir, name)
        os.chdir(api_dir)

        files = ("__init__.py",)
        for file in files:
            fd = os.open(file, os.O_CREAT)
            os.close(fd)

        dirs = ("test_services", "test_repos", "test_schemas", "test_routes")
        for dir_ in dirs:
            os.mkdir(dir_)
            fd = os.open(f"{dir_}/__init__.py", os.O_CREAT)
            os.close(fd)

        print(f"tests {name} created.")
