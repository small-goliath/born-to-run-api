import app.core.converter as converter
import app.infrastructer.marathon_gateway as marathon_gateway
from app.api.deps import SessionDep
from app.models import BookmarkMarathonCommand, MarathonGlobal, SearchMarathonsCommand, SearchMarathonDetailCommand


async def search_marathons(session: SessionDep, command: SearchMarathonsCommand) -> list[MarathonGlobal]:
    query = converter.to_searchMarathonsQuery(command)
    marathons, bookmarks = await marathon_gateway.search_marathons(session, query)

    return converter.to_marathonGlobals(marathons, bookmarks)

async def search_marathon_detail(session: SessionDep, command: SearchMarathonDetailCommand) -> MarathonGlobal:
    query = converter.to_searchMarathonDetailQuery(command)
    marathon, bookmark = await marathon_gateway.search_marathon_detail(session, query)

    return converter.to_marathonGlobal(marathon, bookmark)

async def bookmark(session: SessionDep, command: BookmarkMarathonCommand) -> int:
    query = converter.to_bookmarkMarathonQuery(command)
    bookmarked = await marathon_gateway.bookmark(session, query)

    return bookmarked.marathon_id