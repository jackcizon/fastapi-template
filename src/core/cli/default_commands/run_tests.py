from typing import Any

from click import Context, Command


class RunTestsCommand(Command):
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        # TODO: do it after finishing tests.
        super().__init__(*args, **kwargs)

    def invoke(self, ctx: Context) -> Any:
        return super().invoke(ctx)
