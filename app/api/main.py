from fastapi import APIRouter

from app.api.routes import crews, login

api_router = APIRouter()
api_router.include_router(crews.router, prefix="/crews", tags=["crews"])
api_router.include_router(login.router, prefix="/login", tags=["login"])