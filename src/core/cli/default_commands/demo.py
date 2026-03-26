from typing import Any

from click import Context, Parameter, Option, Argument, Command


class DemoCommand(Command):
    """
    A command for Demo Usage!
    Option and Argument must use cls to init if you need them.
    params: list[Parameter] | None = None,
    Both `Option` and `Argument` are inherit from Parameter

    rule:
    a command cls name must like `*Command`
    """

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)

        self._dict = {"opt": {"demo-opt": ["-d", "--demo-opt"]}, "arg": {"demo-arg": ["demo-arg"]}}
        self.params: list[Parameter] = [
            Option(param_decls=self._dict.get("opt").get("demo-opt"), default="0", type=str),
            Argument(param_decls=self._dict.get("arg").get("demo-arg"), default="0", type=str),
            # others...
        ]
        self.help = "A demo command, see my implementation to know how to use `click`."

    def invoke(self, ctx: Context) -> Any:
        for param in self.params:
            print(f"{param.param_type_name} => {param.name}")

        demo_opt = ctx.params.get("demo-opt")
        demo_arg = ctx.params.get("demo-arg")

        print(f"input demo-opt: {demo_opt}, input demo-arg: {demo_arg}")
        print("it works. please write more cmds in api.<app_name>.default_commands.<custom_cmd.py>")

        return super().invoke(ctx)
