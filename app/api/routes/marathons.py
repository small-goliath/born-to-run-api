from fastapi import APIRouter

import app.core.converter as converter
import app.core.proxy as proxy
from app.api.deps import SessionDep, CurrentUserId
from app.api.routes.schemas import BookmarkMarathonResponse, SearchMarathonDetailResponse, SearchMarathonsRequest

router = APIRouter()

@router.get("")
async def search_marathons(session: SessionDep, my_user_id: CurrentUserId, request: SearchMarathonsRequest = None):
    marathons = await proxy.search_marathons(session, request, my_user_id)
    return converter.to_SearchMarathonsResponse(marathons)

@router.get("/{marathon_id}")
async def search_marathon_detail(session: SessionDep, marathon_id: int, my_user_id: CurrentUserId) -> SearchMarathonDetailResponse:
    marathon = await proxy.search_marathon_detail(session, marathon_id, my_user_id)
    return converter.to_SearchMarathonDetailResponse(marathon)

@router.post("/bookmark/{marathon_id}")
async def bookmark_marathon(session: SessionDep, marathon_id: int, my_user_id: CurrentUserId) -> BookmarkMarathonResponse:
    marathon_id = await proxy.bookmark_marathon(session, marathon_id, my_user_id)
    return BookmarkMarathonResponse(marathon_id=marathon_id)