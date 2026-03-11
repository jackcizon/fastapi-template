# Start Project

Unlike Django, the `fastapi` project doesn't require a separate `manage.py` file for entry points.

While `manage.py` sets up an `ENV` for Django applications, `fastapi` is started by `uvicorn`.

Therefore, you only need to write the `app` instance in `main.py`, the actual entry point of the project.