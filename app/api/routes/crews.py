from fastapi import APIRouter

import app.core.converter as converter
import app.core.proxy as proxy
from app.api.deps import SessionDep
from app.api.routes.schemas import SearchCrewsAllResponse

router = APIRouter()

# TODO: 등록 크루가 많아지면 페이징 적용
@router.get("/")
async def search_crews(session: SessionDep) -> list[SearchCrewsAllResponse]:
    crews = await proxy.search_crews(session)
    return converter.to_searchCrewsAllResponse(crews)