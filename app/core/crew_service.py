import logging
from app.api.deps import SessionDep
from app.models import CrewGlobal
import app.infrastructer.crew_gateway as crew_gateway
import app.core.converter as converter

async def search_crews(session: SessionDep) -> list[CrewGlobal]:
    crews = await crew_gateway.search_crews(session)
    return converter.crew_to_crewGlobal(crews)

async def get_kakao_auth_code() -> str:
    return "kakao_auth_code"