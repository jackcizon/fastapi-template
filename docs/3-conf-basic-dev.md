# Conf Basic Dev

1. Configurations in the `settings`/`config` modules must be imported via `.env`.
This is achieved by dynamically reading `.env` by setting the environment variable `ENV=`dev`/`prod`.

2. FastAPI's `settings cls` is a collection of constants. You can set `cls` yourself,
or use third-party packages, but inheritance relationships cannot be explicitly defined.

3. Export configurations through module-level singleton classes. Configurations must be isolated from the app and
   imported only as needed.

4. Each api's `py files` must have clearly defined responsibilities. Under `tests`, directly copy the structure of
   `api`, and add the `test_` prefix for easier testing and management.