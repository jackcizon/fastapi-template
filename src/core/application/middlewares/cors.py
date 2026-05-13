from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from src.core.config import settings


def setup_cors_middleware(app_: FastAPI) -> None:
    app_.add_middleware(
        # CORSMiddleware has already implemented __call__(), it is ok.
        middleware_class=CORSMiddleware,  # type: ignore
        allow_origins=settings.cors_allow_origins,
        allow_credentials=settings.cors_allow_credentials,
        allow_methods=settings.cors_allow_methods,
        allow_headers=settings.cors_allow_headers,
    )
