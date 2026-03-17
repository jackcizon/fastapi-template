"""register all Commands here."""

from src.core.cli.cli import GlobalCommandsManager, __DemoCommand


def add_commands(manager: GlobalCommandsManager) -> None:
    """
    Explicit is better than implicit.

    register cmds here.
    e.g.:
        manager.add_command(cmd_cls("<name>"))
    """
    manager.add_command(__DemoCommand("demo"))
