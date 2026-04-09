import os
import sys
from typing import Any

import uvicorn
from click import Command, Context, Parameter, Option

from src.core.config import ROOT_DIR


class RunServerCommand(Command):
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)

        sys.path.append(str(ROOT_DIR))
        sys.path.append(os.path.join(ROOT_DIR, "src"))

        self._dict = {"opt": {"host": ["-H", "--host"], "port": ["-p", "--port"]}}
        self.params: list[Parameter] = [
            Option(param_decls=self._dict.get("opt").get("host"), default="0.0.0.0", type=str),
            Option(param_decls=self._dict.get("opt").get("port"), default=8000, type=int),
        ]
        self.help = "run dev server"

    def invoke(self, ctx: Context) -> Any:
        host = ctx.params.get("host")
        port = ctx.params.get("port")
        uvicorn.run("main:app", host=host, port=port, reload=True, factory=True, reload_dirs=["src"])
        return super().invoke(ctx)
