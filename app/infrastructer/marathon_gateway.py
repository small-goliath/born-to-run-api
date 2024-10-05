import logging

from sqlmodel import and_, select

from app.api.deps import SessionDep
from app.models import SearchMarathonsQuery, Marathon, MarathonBookmark


async def search_marathons(session: SessionDep, query: SearchMarathonsQuery) -> tuple[list[Marathon], list[MarathonBookmark]]:
    logging.debug(f"Try to search marathons: {query}")

    statement = select(Marathon, MarathonBookmark).join(MarathonBookmark, isouter=True, onclause=and_(Marathon.id == MarathonBookmark.marathon_id, MarathonBookmark.user_id == query.my_user_id))
    result = session.exec(statement).all()

    marathons = [marathon for marathon, _ in result if marathon is not None]
    bookmarks = [bookmark for _, bookmark in result if bookmark is not None]

    logging.debug(f"found marathons: {", ".join(str(marathon.id) for marathon in marathons)}")
    logging.debug(f"found marathon bookmarks: {", ".join(str(bookmark.marathon_id) for bookmark in bookmarks)}")

    return marathons, bookmarks