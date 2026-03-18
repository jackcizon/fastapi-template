from typing import Any

from click import Command, Group


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
        if isinstance(cmd, Command) or issubclass(type(cmd), type(Command)):
            super().add_command(cmd, name)  # type: ignore

    def discover_commands(self) -> None:
        raise NotImplementedError("Not prepare to implement this method.")

    def __call__(self, *args: Any, **kwargs: Any) -> Any:
        """if not implement this __call__, you need do like:
        e.g.:
        manager = CommandsManager()
        # add some commands manually or auto discover.
        manager()
        """
        return self.main(*args, **kwargs)
