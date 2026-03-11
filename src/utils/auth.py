from fastapi import HTTPException, Request
from jwt import ExpiredSignatureError, InvalidTokenError

from src.utils.datastructures import JSONWebToken


def get_current_user(request: Request) -> str:
    """
    :param request: FastAPI Request
    :return: str: user.open_id
    """
    auth = request.headers.get("Authorization")
    if not auth or not auth.startswith("Bearer "):
        raise HTTPException(401, "Not authenticated")

    token = auth.split(" ", 1)[1]

    try:
        payload = JSONWebToken().decode_token(token=token)
    except ExpiredSignatureError:
        raise HTTPException(401, "Token expired")
    except InvalidTokenError:
        raise HTTPException(401, "Invalid token")

    # 2. payload type check
    if payload.get("type") != "access":
        raise HTTPException(status_code=401, detail="token type must be access")
    user_open_id = payload.get("id")
    if not user_open_id:
        raise HTTPException(401, "Invalid token payload")

    return user_open_id
