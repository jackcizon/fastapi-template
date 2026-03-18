from typing import Any

from click import Context, Parameter, Option, Argument, Command


class DemoCommand(Command):
    """
    A command for Demo Usage!
    Option and Argument must use cls to init if you need them.
    params: list[Parameter] | None = None,
    Both `Option` and `Argument` are inherit from Parameter
    """

    def __init__(self, name: str, *args: Any, **kwargs: Any) -> None:
        super().__init__(name, *args, **kwargs)

        self.params: list[Parameter] = [
            Option(param_decls=["-d", "--demo-opt"], default="0", type=str),
            Argument(param_decls=["demo-arg"], default="0", type=str),
            # others...
        ]
        self.help = "A demo command, see my implementation to know how to use `click`."

    def invoke(self, ctx: Context) -> Any:
        super().invoke(ctx)
        for param in self.params:
            print(f"{param.param_type_name} => {param.name}")
        print("it works. please write more cmds in apps.<app_name>.default_commands.<custom_cmd.py>")
