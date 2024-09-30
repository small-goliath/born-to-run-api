from fastapi import APIRouter, Depends

from app.api.deps import SessionDep, get_current_user
from app.api.routes.schemas import SearchMyDetailResponse
import app.core.converter as converter
import app.core.proxy as proxy

router = APIRouter()

@router.get("/my")
async def search_my_detail(session: SessionDep, my_user_id=Depends(get_current_user)) -> SearchMyDetailResponse:
    user = await proxy.get_user_detail(session, my_user_id)
    return converter.userGlobal_to_searchMyDetailResponse(user)