import os
from typing import Any

from click import Context, Command


class RunTestsCommand(Command):
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)

    def invoke(self, ctx: Context) -> Any:
        os.system("make test")
        return super().invoke(ctx)
