from fastapi import APIRouter
from fastapi.params import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.responses import JSONResponse

from src.api.rbac.models import User
from src.api.user.schemas.avatar_schema import (
    AvatarUploadRequestSchema,
    AvatarUploadCallbackRequestSchema,
    AvatarUploadCallbackResponseSchema,
    AvatarUploadResponseSchema,
)
from src.api.user.services.avatar_service import AvatarService
from src.core.db.session import get_db
from src.core.securities.jwt import jwt_required_dep

avatar_router = APIRouter()


@avatar_router.post("/avatar/upload/", name="user:avatar_upload:post")
async def avatar_upload(req: AvatarUploadRequestSchema, user: User = Depends(jwt_required_dep)) -> JSONResponse:
    """
    ```
    step 1:
    post `/user/avatar/upload/`, add header(Bearer),
    send json: `{"filename": "<filename>.png"}`
    get return json: `{
        "put_url": "<s3_server_ip>/<bucket(must create firstly)>/user/<id>/avatar/<uuid>.png?<query_params>",
        "key": "user/2045051385950638080/avatar/7c6b2854bbac4657b7faccae0226d6f4.png"
    }`

    step 2:
    put `put_url`, add header(Content-Type: image/png)
    get resp status code == 200, ok.
    ```
    """
    resp_dict = await AvatarService.upload(req.model_dump(), user.id)
    return JSONResponse(content=AvatarUploadResponseSchema(**resp_dict).model_dump())


@avatar_router.post("/avatar/upload/callback/", name="user:avatar_upload_completed:post")
async def avatar_upload_callback(
    req: AvatarUploadCallbackRequestSchema, db: AsyncSession = Depends(get_db), user: User = Depends(jwt_required_dep)
) -> JSONResponse:
    """
    Do in postman.

    ```txt
    post: {
        "key": "user/2045051385950638080/avatar/7c6b2854bbac4657b7faccae0226d6f4.png"
    }
    return json: {
        "avatar_url": "http://localhost:9000/fastapi-template/user/2045051385950638080/avatar/7c6b2854bbac4657b7faccae0226d6f4.png?AWSAccessKeyId=admin&Signature=f%2B2WJ6xBmyYlVXaf7hxQ9d8ssxw%3D&Expires=1776497061"
    }
    ```

    :param req: send from frontend, {"key": "user/2045051385950638080/avatar/7c6b2854bbac4657b7faccae0226d6f4.png"}
    :param db:
    :param user:
    :return:
    """
    resp_dict = await AvatarService.upload_callback(req.model_dump(), user.id, db)
    return JSONResponse(content=AvatarUploadCallbackResponseSchema(**resp_dict).model_dump())
