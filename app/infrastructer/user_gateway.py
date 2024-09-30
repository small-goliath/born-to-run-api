from sqlmodel import select

from app.api.deps import SessionDep
from app.models import Authority, Crew, ObjectStorage, User, UserPrivacy
import logging

async def search_user(session: SessionDep, my_user_id: int) -> User:
    statement = select(User, Crew, ObjectStorage).select_from(User).where(User.id == my_user_id).join(Crew).join(ObjectStorage, isouter=True).join(UserPrivacy, isouter=True).join(Authority, isouter=True)
    user = session.exec(statement).one()

    logging.debug(f"found user: {user}")
    
    return user