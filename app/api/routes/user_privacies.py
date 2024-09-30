from fastapi import APIRouter, Depends

from app.api.deps import SessionDep, get_current_user
from app.api.routes.schemas import ModifyUserPrivacyRequest, SearchUserPrivacyResponse
import app.core.converter as converter
import app.core.proxy as proxy

router = APIRouter()

@router.post("/privacy/user")
async def modify_user_privacy(session: SessionDep, request: ModifyUserPrivacyRequest, my_user_id=Depends(get_current_user)):
    await proxy.modify_user_privacy(session, my_user_id, request)

@router.get("/privacy/user")
async def search_user_privacy(session: SessionDep, my_user_id=Depends(get_current_user)) -> SearchUserPrivacyResponse:
    searched = await proxy.search_user_privacy(session, my_user_id)
    return converter.to_searchUserPrivacyResponse(searched)