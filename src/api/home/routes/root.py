from fastapi import APIRouter
from starlette.responses import JSONResponse

root_router = APIRouter()


@root_router.get("/", name="home:root:get")
def root() -> JSONResponse:
    return JSONResponse(content={"home": "root"})
