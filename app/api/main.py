from fastapi import APIRouter

from app.api.routes import crews

api_router = APIRouter()
api_router.include_router(crews.router, prefix="/crews", tags=["crews"])