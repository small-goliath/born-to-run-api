from fastapi import APIRouter, Depends

import app.core.converter as converter
import app.core.proxy as proxy
from app.api.deps import SessionDep, get_current_user
from app.api.routes.schemas import SearchMarathonsRequest

router = APIRouter()

@router.get("")
async def search_marathons(session: SessionDep, my_user_id=Depends(get_current_user), request: SearchMarathonsRequest = None):
    marathons = await proxy.search_marathons(session, request, my_user_id)
    return converter.to_SearchMarathonsResponse(marathons)