from fastapi import APIRouter, Response

import app.core.converter as converter
import app.core.proxy as proxy
from app.api.deps import SessionDep, CurrentUserId
from app.api.routes.schemas import ModifyUserPrivacyRequest, SearchUserPrivacyResponse

router = APIRouter()

@router.put("/user")
async def modify_user_privacy(session: SessionDep, request: ModifyUserPrivacyRequest, my_user_id: CurrentUserId):
    await proxy.modify_user_privacy(session, my_user_id, request)
    return Response(status_code=200)

@router.get("/user")
async def search_user_privacy(session: SessionDep, my_user_id: CurrentUserId) -> SearchUserPrivacyResponse:
    searched = await proxy.search_user_privacy(session, my_user_id)
    return converter.to_searchUserPrivacyResponse(searched)