from fastapi import APIRouter

from app.models import SearchCrewsAllResponse
from app.api.deps import SessionDep
import app.core.converter as converter
import app.core.proxy as proxy

router = APIRouter()

# TODO: 등록 크루가 많아지면 페이징 적용
@router.get("/")
async def search_crews(session: SessionDep) -> list[SearchCrewsAllResponse]:
    crews = await proxy.search_crews(session)
    return converter.crewGlobal_to_searchCrewsAllResponse(crews)