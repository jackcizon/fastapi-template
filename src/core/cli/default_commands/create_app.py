import os
from typing import Any

from click import Context, Command, Parameter, Option

from src.core.config import SRC_DIR


class CreateAppCommand(Command):
    def __init__(self, name: str, *args: Any, **kwargs: Any) -> None:
        super().__init__(name, *args, **kwargs)

        self._dict = {"opt": {"name": ["-n", "--name"]}, "arg": {}}
        self.params: list[Parameter] = [
            Option(param_decls=self._dict.get("opt").get("name"), type=str),
        ]
        self.help = "create a app"

    def invoke(self, ctx: Context) -> Any:
        name = ctx.params.get("name")
        print(f"try creating app:{name}....")
        try:
            target_dir = os.path.join(SRC_DIR, "apps")
            os.chdir(target_dir)
            os.mkdir(name)
            app_dir = os.path.join(target_dir, name)
            os.chdir(app_dir)

            files = (
                "__init__.py",
                "routes.py",
                "repos.py",
                "services.py",
                "models.py",
                "schemas.py",
            )
            for file in files:
                fd = os.open(file, os.O_CREAT)
                os.close(fd)
            print(f"new app:{name} created.")
        except Exception as e:
            print(e)
            raise
        finally:
            return super().invoke(ctx)
