from fastapi import APIRouter

from api.v1.endpoints import users
from api.v1.endpoints import artigos

api_router = APIRouter()

api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(artigos.router, prefix="/artigos", tags=["artigos"])