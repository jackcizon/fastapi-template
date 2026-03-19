"""register all Commands here."""

from src.core.cli.manager import GlobalCommandsManager


def add_default_commands(manager: GlobalCommandsManager) -> None:
    manager.discover_commands()


def add_commands(manager: GlobalCommandsManager) -> None:
    """
    Explicit is better than implicit.

    add manually(any importable path in this project) or auto discover(must locate in `src.apps.<app_name>.commands`).

    register cmds here.
    e.g.:
        manager.add_command(cmd_cls("<name>"))
    """
    add_default_commands(manager)
    manager.discover_commands("src/apps/rbac/commands")
