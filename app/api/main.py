from fastapi import APIRouter

from app.api.routes import crews, join, users

api_router = APIRouter()
api_router.include_router(crews.router, prefix="/crews", tags=["crews"])
api_router.include_router(join.router, prefix="/join", tags=["join"])
api_router.include_router(users.router, prefix="/users", tags=["users"])