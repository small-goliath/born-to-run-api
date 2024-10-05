from fastapi import APIRouter, Depends

import app.core.converter as converter
import app.core.proxy as proxy
from app.api.deps import SessionDep, get_current_user, CurrentUserId
from app.api.routes.schemas import ModifyUserRequest, ModifyUserResponse, SearchMyDetailResponse

router = APIRouter()

@router.get("/my")
async def search_my_detail(session: SessionDep, my_user_id=CurrentUserId) -> SearchMyDetailResponse:
    user = await proxy.get_user_detail(session, my_user_id)
    return converter.to_searchMyDetailResponse(user)

@router.get("/{user_id: int}")
async def search_user_detail(session: SessionDep, user_id: int) -> SearchMyDetailResponse:
    user = await proxy.get_user_detail(session, user_id)
    return converter.to_searchMyDetailResponse(user)

@router.put("/my")
async def modify_user(session: SessionDep, request: ModifyUserRequest, user_id=CurrentUserId) -> ModifyUserResponse:
    modified_user_name = await proxy.modify_user(session, user_id, request)
    return ModifyUserResponse(userName=modified_user_name)