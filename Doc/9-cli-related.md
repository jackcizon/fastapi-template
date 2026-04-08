# CLI Related

To simulate a Django-like command-line interface, we first need a `manage.py` entry point.

In order to automatically discovering all commands within each api,

we need some modules, like `inspect` and `importlib`.

For example, a command is located in `src/api/rbac/commands/filename.py`.

Do not place commands in packages like `commands/api1`, `commands/api2`, etc.

For structs, wrap `click.command` with classes, not just functions with decorators.

Discover and read all py-files in `api_name.commands`.

## Hint

But for simple and robust, I will use global Singleton, return a CommandManager, explicit add commands.

## Warning

Do Not Use `click` Docorator.
