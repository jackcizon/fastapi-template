from fastapi import FastAPI
from src.core.exceptions.auth import AuthError
from src.core.exceptions.handlers.auth import auth_error_handler


def add_exception_handlers(app_: FastAPI) -> None:
    app_.add_exception_handler(AuthError, auth_error_handler)
