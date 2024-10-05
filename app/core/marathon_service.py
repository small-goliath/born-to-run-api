import app.core.converter as converter
import app.infrastructer.marathon_gateway as marathon_gateway
from app.api.deps import SessionDep
from app.models import MarathonGlobal, SearchMarathonsCommand

async def search_marathons(session: SessionDep, command: SearchMarathonsCommand) -> list[MarathonGlobal]:
    query = converter.to_searchMarathonsQuery(command)
    marathons, bookmarks = await marathon_gateway.search_marathons(session, query)

    return converter.to_marathonGlobal(marathons, bookmarks)