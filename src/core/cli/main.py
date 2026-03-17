from src.core.cli.cli import GlobalCommandsManager
from src.core.cli.registry import add_commands


def execute_from_cli() -> None:
    manager = GlobalCommandsManager()
    add_commands(manager)
    manager.main()
