from datetime import datetime, timezone
from typing import Any

import jwt

from src.core.config import infra_settings


class JSONWebToken:
    @staticmethod
    def create_access_token(id_: str | int) -> str:  #  pragma: no cover
        payload = {
            "id": id_,
            "exp": int(datetime.now(tz=timezone.utc).timestamp()) + infra_settings.ACCESS_TOKEN_TTL,
            "iat": int(datetime.now(tz=timezone.utc).timestamp()),
            "type": "access",
        }
        return jwt.encode(
            payload=payload, key=infra_settings.JWT_KEY, algorithm=infra_settings.JWT_ALGO
        )

    @staticmethod
    def create_refresh_token(id_: str | int) -> str:  # pragma: no cover
        payload = {
            "id": id_,
            "exp": int(datetime.now(tz=timezone.utc).timestamp())
            + infra_settings.REFRESH_TOKEN_TTL,
            "iat": int(datetime.now(tz=timezone.utc).timestamp()),
            "type": "refresh",
        }
        return jwt.encode(
            payload=payload, key=infra_settings.JWT_KEY, algorithm=infra_settings.JWT_ALGO
        )

    def decode_token(self, token: str, token_type: str | None = None) -> dict[str, Any]:
        try:
            payload = jwt.decode(
                jwt=token, key=infra_settings.JWT_KEY, algorithms=[infra_settings.JWT_ALGO]
            )
            if token_type is not None:
                if payload.get("type") != token_type:
                    raise jwt.InvalidKeyError("payload key:val error")
                # if self.in_blacklist(token):
                #     raise jwt.InvalidTokenError('token is in blacklist')
            return payload
        except jwt.ExpiredSignatureError:
            raise jwt.ExpiredSignatureError("token expired")
        except jwt.InvalidTokenError:
            raise jwt.InvalidTokenError("invalid token")

    # @staticmethod
    # def in_blacklist(token: str) -> bool:
    #     return False
    #
    # def join_token_in_blacklist(self, token: str) -> None:
    #     # set token in redis blacklist
    #     return
