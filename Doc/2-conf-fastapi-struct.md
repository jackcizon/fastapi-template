# Conf FastAPI Struct

1. The combination of `url.py` and `views.py` is no longer acceptable; this is an anti-pattern. Use `routes.py` instead.

2. The separation of app startup and the main `urls.py` is no longer necessary. Add the routing table directly after app
   instantiation.

3. In PyCharm's configuration, set the startup directory to the directory containing `main.py` and set `PYTHONPATH=src`.
   This eliminates the need to specify `src`.

4. Start the module `uvicorn` at the `module` level. Fill in the relevant startup parameters in `parameters` (see
   `uvicorn --help` for details).

5. Step 3 works in Django, but it still requires inserting into `sys.path`, which violates FastAPI principles. In
   FastAPI, packages can be directly imported from `src`. Otherwise, subsequent testing will encounter problems (due to
   pip's import principles).