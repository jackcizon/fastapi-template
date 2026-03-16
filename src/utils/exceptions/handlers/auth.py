from starlette.responses import JSONResponse


def auth_error_handler(request, exc):
    return JSONResponse(status_code=401, content={'detail': "Auth Error"})
