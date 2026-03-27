from typing import Any

from click import Command, Context, echo
from fastapi.routing import APIRoute
from starlette.routing import Route

from src.main import app


class ListRoutesCommand(Command):
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)

    def invoke(self, ctx: Context) -> Any:
        app_routes: list[Route | APIRoute | Any] = app.instance.routes
        for app_route in app_routes:
            echo(app_route)
        super().invoke(ctx)
