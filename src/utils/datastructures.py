from datetime import datetime
from typing import TypeVar, TypeAlias, Any

import jwt

from src.core.config import infra_settings

TokenPair: TypeVar = TypeVar(name="TokenPair", bound=Any)


class JSONWebToken:
    @staticmethod
    def create_access_token(id_: int):
        payload = {
            'id': id_,
            'exp': datetime.now() + infra_settings.ACCESS_TOKEN_TTL,
            'iat': datetime.now(),
            'type': 'access'
        }
        return jwt.encode(payload=payload, key=infra_settings.JWT_KEY, algorithm=infra_settings.JWT_ALGO)

    @staticmethod
    def create_refresh_token(id_: int):
        payload = {
            'id': id_,
            'exp': datetime.now() + infra_settings.REFRESH_TOKEN_TTL,
            'iat': datetime.now(),
            'type': 'refresh'
        }
        return jwt.encode(payload=payload, key=infra_settings.JWT_KEY, algorithm=infra_settings.JWT_ALGO)

    def decode_token(self, token: str, token_type: str | None = None):
        try:
            payload = jwt.decode(jwt=token, key=infra_settings.JWT_KEY, algorithms=[infra_settings.JWT_ALGO])
            if token_type is not None:
                if payload.get('type') != token_type:
                    raise jwt.InvalidKeyError('payload key:val error')
                if self.in_blacklist(token):
                    raise jwt.InvalidTokenError('token is in blacklist')
            return payload
        except jwt.ExpiredSignatureError:
            raise jwt.ExpiredSignatureError('token expired')
        except jwt.InvalidTokenError:
            raise jwt.InvalidTokenError('invalid token')
        finally:
            raise jwt.DecodeError('decode error')

    @staticmethod
    def in_blacklist(token: str) -> bool:
        # get token from redis cache
        token_ = token  # pass
        return False

    def join_token_in_blacklist(self, token: str) -> str:
        # set token in redis blacklist
        token_ = token  # pass
        return token_
