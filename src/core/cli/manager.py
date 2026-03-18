import os
import inspect
from importlib import import_module
from typing import Any

from click import Command, Group

from src.core.config import ROOT_DIR


class GlobalCommandsManager(Group):
    """
    do not use @click.group() decorator,
    it's a helper function that hides the underlying implementation,
    its source code return a Group instance.
    """

    _instance = None

    def __new__(cls, *args: Any, **kwargs: Any) -> Any:
        if not cls._instance:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        """see params in super cls."""
        super().__init__(*args, **kwargs)

    def add_command(self, cmd: Command | Any, name: str | None = None) -> None:
        if isinstance(cmd, Command) or issubclass(cmd, Command):
            super().add_command(cmd, name)  # type: ignore

    def discover_commands(
        self, path_from_project_root: str = "src/core/cli/default_commands"
    ) -> None:
        """
        default path should in src/core/cli/default_commands

        command style is CamelCase.
        """
        module_from_project_root = path_from_project_root.replace(
            "/", "."
        )  # src/core/cli/default_commands -> src.core.cli.default_commands
        cmds_abs_path = os.path.join(ROOT_DIR, path_from_project_root)  # /path/to/default_commands

        try:
            for file in os.listdir(cmds_abs_path):
                if not file.endswith(".py"):
                    continue

                filename = file.split(".")[0]  # demo.py -> demo
                file_module = (
                    f"{module_from_project_root}.{filename}"  # src.core.cli.default_commands.demo
                )
                module = import_module(file_module)

                members = inspect.getmembers(module, inspect.isclass)
                for member in members:
                    member_cls_str = member[0]
                    member_cls = member[1]

                    if (
                        issubclass(member_cls, Command)
                        and member_cls_str.endswith("Command")  # custom Command rule
                        and len(member_cls_str) > len("Command")  # ignore click.core.Command
                    ):
                        # DemoCommand -> Demo. CamelCase
                        self.add_command(member_cls(name=member_cls_str.replace("Command", "")))
        except Exception as e:
            print(e)
            raise

    def __call__(self, *args: Any, **kwargs: Any) -> Any:
        """if not implement this __call__, you need do like:
        e.g.:
        manager = CommandsManager()
        # add some commands manually or auto discover.
        manager()
        """
        return self.main(*args, **kwargs)
