from sqlmodel import select

from app.api.deps import SessionDep
from app.models import Crew, ObjectStorage
import logging

async def search_crews(session: SessionDep) -> list[Crew]:
    statement = select(Crew, ObjectStorage).join(ObjectStorage, isouter=True)
    crews = session.exec(statement).all()
    logging.debug(f"found crews: {crews}")
    
    return list(crews)