"""register all Commands here."""

from src.core.cli.manager import GlobalCommandsManager
from src.core.cli.default_commands.demo import DemoCommand
from src.core.cli.default_commands.create_app import CreateAppCommand
from src.core.cli.default_commands.run_server import RunServerCommand


def add_default_commands(manager: GlobalCommandsManager) -> None:
    manager.add_command(DemoCommand("demo"))
    manager.add_command(CreateAppCommand("create_app"))
    manager.add_command(RunServerCommand("run_server"))
    # manager.discover_commands()


def add_commands(manager: GlobalCommandsManager) -> None:
    """
    Explicit is better than implicit.

    register cmds here.
    e.g.:
        manager.add_command(cmd_cls("<name>"))
    """
    manager.add_command(__DemoCommand("demo"))
