from typing import Any
from datetime import datetime, timezone

import jwt

from src.core.config import settings


class JSONWebToken:
    @staticmethod
    def create_access_token(id_: str | int) -> str:
        payload = {
            "id": id_,
            "exp": int(datetime.now(tz=timezone.utc).timestamp()) + settings.access_token_ttl,
            "iat": int(datetime.now(tz=timezone.utc).timestamp()),
            "type": "access",
        }
        return jwt.encode(payload=payload, key=settings.jwt_key, algorithm=settings.jwt_algo)

    @staticmethod
    def create_refresh_token(id_: str | int) -> str:  # pragma: no cover
        payload = {
            "id": id_,
            "exp": int(datetime.now(tz=timezone.utc).timestamp()) + settings.refresh_token_ttl,
            "iat": int(datetime.now(tz=timezone.utc).timestamp()),
            "type": "refresh",
        }
        return jwt.encode(payload=payload, key=settings.jwt_key, algorithm=settings.jwt_algo)

    @staticmethod
    def decode_token(token: str, token_type: str | None = None) -> dict[str, Any]:
        try:
            payload = jwt.decode(jwt=token, key=settings.jwt_key, algorithms=[settings.jwt_algo])
            if token_type is not None:
                if payload.get("type") != token_type:
                    raise jwt.InvalidKeyError("payload key:val error")
            return payload
        except jwt.ExpiredSignatureError:
            raise jwt.ExpiredSignatureError("token expired")
        except jwt.InvalidTokenError:
            raise jwt.InvalidTokenError("invalid token")
