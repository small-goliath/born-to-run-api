import app.core.converter as converter
import app.infrastructer.crew_gateway as crew_gateway
from app.api.deps import SessionDep
from app.models import CrewGlobal


async def search_crews(session: SessionDep) -> list[CrewGlobal]:
    crews = await crew_gateway.search_crews(session)
    return converter.to_crewGlobal(crews)