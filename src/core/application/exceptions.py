from fastapi import FastAPI

from src.core.exceptions.auth import AuthError
from src.core.exceptions.bad_request import BadRequestError
from src.core.exceptions.datetime_ import DateTimeError
from src.core.exceptions.db import DBError
from src.core.exceptions.handlers.auth import auth_error_handler
from src.core.exceptions.handlers.bad_request import bad_request_error_handler
from src.core.exceptions.handlers.datetime_ import datetime_error_handler
from src.core.exceptions.handlers.db import db_error_handler
from src.core.exceptions.handlers.jwt import jwt_error_handler
from src.core.exceptions.handlers.not_found import not_found_error_handler
from src.core.exceptions.jwt import JWTError
from src.core.exceptions.not_found import NotFoundError


def add_exception_handlers(app_: FastAPI) -> None:
    app_.add_exception_handler(AuthError, auth_error_handler)
    app_.add_exception_handler(JWTError, jwt_error_handler)
    app_.add_exception_handler(DateTimeError, datetime_error_handler)
    app_.add_exception_handler(NotFoundError, not_found_error_handler)
    app_.add_exception_handler(DBError, db_error_handler)
    app_.add_exception_handler(BadRequestError, bad_request_error_handler)
