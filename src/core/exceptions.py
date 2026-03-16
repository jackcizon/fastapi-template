from fastapi import FastAPI
from src.utils.exceptions.auth import AuthError
from src.utils.exceptions.handlers.auth import auth_error_handler


def add_exception_handlers(app_: FastAPI):
    app_.add_exception_handler(AuthError, auth_error_handler)
