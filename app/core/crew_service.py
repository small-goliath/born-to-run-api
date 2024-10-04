from app.api.deps import SessionDep
from app.models import CrewGlobal
import app.infrastructer.crew_gateway as crew_gateway
import app.core.converter as converter

async def search_crews(session: SessionDep) -> list[CrewGlobal]:
    crews = await crew_gateway.search_crews(session)
    return converter.to_crewGlobal(crews)