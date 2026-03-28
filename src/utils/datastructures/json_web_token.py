from typing import Any
from datetime import datetime, timezone

import jwt

from src.core.config import settings
from src.core.exceptions.jwt import JWTError


class JSONWebToken:
    @staticmethod
    def create_access_token(id_: str | int) -> str:
        payload = {
            "user_id": id_,
            "exp": int(datetime.now(tz=timezone.utc).timestamp()) + settings.access_token_ttl,
            "iat": int(datetime.now(tz=timezone.utc).timestamp()),
            "type": "access",
        }
        try:
            return jwt.encode(payload=payload, key=settings.jwt_key, algorithm=settings.jwt_algo)
        except (Exception, TypeError):
            raise JWTError("Jwt Encode error")

    @staticmethod
    def create_refresh_token(id_: str | int) -> str:  # pragma: no cover
        payload = {
            "user_id": id_,
            "exp": int(datetime.now(tz=timezone.utc).timestamp()) + settings.refresh_token_ttl,
            "iat": int(datetime.now(tz=timezone.utc).timestamp()),
            "type": "refresh",
        }
        try:
            return jwt.encode(payload=payload, key=settings.jwt_key, algorithm=settings.jwt_algo)
        except (Exception, TypeError):
            raise JWTError("Jwt encode error")

    @staticmethod
    def decode_token(token: str, token_type: str | None = None) -> dict[str, Any]:
        try:
            payload = jwt.decode(jwt=token, key=settings.jwt_key, algorithms=[settings.jwt_algo])
            if token_type is not None:
                if payload.get("type") != token_type:
                    raise jwt.InvalidKeyError("payload key:val error")
            return payload
        # catch their exceptions, raise your custom defined exception.
        except jwt.ExpiredSignatureError:
            raise JWTError("token expired")
        except jwt.InvalidTokenError:
            raise JWTError("invalid token")
        except Exception:
            raise JWTError("JWT Error")

    @staticmethod
    def generate_token_pair(id_: int | str) -> tuple[str, str]:
        if isinstance(id_, str):
            id_ = int(id_)
        access = JSONWebToken.create_access_token(id_)
        refresh = JSONWebToken.create_refresh_token(id_)
        return access, refresh
