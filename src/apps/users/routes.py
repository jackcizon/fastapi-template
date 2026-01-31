from fastapi.routing import APIRouter

users_router = APIRouter()


@users_router.get('/')
async def users():
    return [{
        '1': 'jack',
        '2': 'john',
        '3': 'musk'
    }]
