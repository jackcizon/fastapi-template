from fastapi import HTTPException, Request
from jwt import ExpiredSignatureError, InvalidTokenError

from src.apps.rbac.models import User
from src.apps.rbac.repos.user_repo import UserRepo
from src.core.db.session import SessionLocal
from src.utils.datastructures.json_web_token import JSONWebToken


def jwt_required_dep(request: Request) -> User:
    """
    :param request: FastAPI Request
    :return: str: user_id
    """
    auth = request.headers.get("Authorization")
    if not auth or not auth.startswith("Bearer "):
        raise HTTPException(401, "Not authenticated")

    token = auth.split(" ")[1]

    try:
        payload = JSONWebToken.decode_token(token)
    except ExpiredSignatureError:
        raise HTTPException(401, "Token expired")
    except InvalidTokenError:
        raise HTTPException(401, "Invalid token")

    # 2. payload type check
    if payload.get("type") != "access":
        raise HTTPException(status_code=401, detail="token type must be access")
    user_id = payload.get("user_id")

    with SessionLocal() as db:
        try:
            user = UserRepo(db).get_by_id(user_id)
        except Exception as e:
            print(e)
            db.rollback()
            raise
        finally:
            db.close()

    if not user_id or user is None:
        raise HTTPException(401, "Invalid token payload")

    return user
