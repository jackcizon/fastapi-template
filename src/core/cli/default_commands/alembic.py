import os
import subprocess
from typing import Any

from click import Context, Parameter, Argument, Command, Option


class AlembicInitCommand(Command):
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)

        self._dict = {"arg": {"directory": ["directory"]}}
        self.params: list[Parameter] = [
            Argument(param_decls=self._dict["arg"]["directory"], default="src/apps/migrations", type=str)
        ]

    def invoke(self, ctx: Context) -> Any:
        directory = ctx.params.get("directory")
        subprocess.run(["alembic", "init", str(directory)])
        return super().invoke(ctx)


class AlembicCheckCommand(Command):
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)

    def invoke(self, ctx: Context) -> Any:
        os.system("alembic check")
        return super().invoke(ctx)


class MakeMigrationsCommand(Command):
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)

        self._dict = {"opt": {"message": ["-m", "--message"], "version_path": ["--version-path"]}}
        self.params: list[Parameter] = [
            Option(param_decls=self._dict["opt"]["message"], default="empty message", type=str),
            Option(
                param_decls=self._dict["opt"]["version_path"],
                default="src/apps/migrations/versions",
                type=str,
            ),
        ]

    def invoke(self, ctx: Context) -> Any:
        message = ctx.params.get("message")
        version_path = ctx.params.get("version_path")
        subprocess.run(
            [
                "alembic",
                "revision",
                "--autogenerate",
                "--version-path",
                str(version_path),
                "-m",
                str(message),
            ]
        )
        return super().invoke(ctx)


class MigrateCommand(Command):
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)

    def invoke(self, ctx: Context) -> Any:
        os.system("alembic upgrade head")
        return super().invoke(ctx)
