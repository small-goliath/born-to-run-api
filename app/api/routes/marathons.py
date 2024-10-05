from fastapi import APIRouter, Depends

import app.core.converter as converter
import app.core.proxy as proxy
from app.api.deps import SessionDep, get_current_user, CurrentUserId
from app.api.routes.schemas import SearchMarathonsRequest
from app.models import SearchMarathonDetailResponse

router = APIRouter()

@router.get("")
async def search_marathons(session: SessionDep, my_user_id: CurrentUserId, request: SearchMarathonsRequest = None):
    marathons = await proxy.search_marathons(session, request, my_user_id)
    return converter.to_SearchMarathonsResponse(marathons)

@router.get("/{marathon_id}")
async def search_marathon_detail(session: SessionDep, marathon_id: int, my_user_id: CurrentUserId) -> SearchMarathonDetailResponse:
    marathon = await proxy.search_marathon_detail(session, marathon_id, my_user_id)
    return converter.to_SearchMarathonDetailResponse(marathon)