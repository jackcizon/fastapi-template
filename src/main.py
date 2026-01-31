"""entry point for FastAPI APP"""
from fastapi import FastAPI

from apps.users.routes import users_router

app = FastAPI(debug=True)

app.include_router(router=users_router, prefix='/users', tags=['users'])
