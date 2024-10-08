import logging

from sqlmodel import and_, select

from app.api.deps import SessionDep
from app.models import BookmarkMarathonQuery, SearchMarathonsQuery, Marathon, MarathonBookmark, \
    SearchMarathonDetailQuery


async def search_marathons(session: SessionDep, query: SearchMarathonsQuery) -> tuple[list[Marathon], list[MarathonBookmark]]:
    logging.debug(f"Try to search marathons: {query}")

    statement = select(Marathon, MarathonBookmark).join(MarathonBookmark, isouter=True, onclause=and_(Marathon.id == MarathonBookmark.marathon_id, MarathonBookmark.user_id == query.my_user_id))
    result = session.exec(statement).all()

    marathons = [marathon for marathon, _ in result if marathon is not None]
    bookmarks = [bookmark for _, bookmark in result if bookmark is not None]

    logging.debug(f"found marathons: {", ".join(str(marathon.id) for marathon in marathons)}")
    logging.debug(f"found marathon bookmarks: {", ".join(str(bookmark.marathon_id) for bookmark in bookmarks)}")

    return marathons, bookmarks

async def search_marathon_detail(session: SessionDep, query: SearchMarathonDetailQuery) -> tuple[Marathon, MarathonBookmark]:
    logging.debug(f"Try to search marathon detail: {query}")

    statement = select(Marathon, MarathonBookmark).where(Marathon.id == query.marathon_id).join(MarathonBookmark, isouter=True, onclause=and_(Marathon.id == MarathonBookmark.marathon_id, MarathonBookmark.user_id == query.my_user_id))
    result = session.exec(statement).one()

    return result

async def bookmark(session: SessionDep, query: BookmarkMarathonQuery) -> MarathonBookmark:
    logging.debug(f"Try to bookmark marathon: {query}")

    bookmarked = MarathonBookmark(marathon_id=query.marathon_id, user_id=query.my_user_id)

    session.add(bookmarked)
    session.commit()
    logging.debug(f"SUCCESS to bookmark marathon: {bookmarked}")

    return bookmarked

async def cancel_bookmark(session: SessionDep, query: BookmarkMarathonQuery) -> MarathonBookmark:
    logging.debug(f"Try to cancel bookmark marathon: {query}")

    statement = select(MarathonBookmark).where(and_(Marathon.id == query.marathon_id, MarathonBookmark.user_id == query.my_user_id))
    marathon_bookmark = session.exec(statement).one()

    marathon_bookmark.is_deleted = True

    session.add(marathon_bookmark)
    session.commit()
    logging.debug(f"SUCCESS to cancel bookmark marathon: {marathon_bookmark}")

    return marathon_bookmark