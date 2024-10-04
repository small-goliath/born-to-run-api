import logging

from sqlmodel import select

from app.api.deps import SessionDep
from app.models import Authority, Crew, ModifyUserQuery, ObjectStorage, User, UserPrivacy


async def search_user(session: SessionDep, user_id: int) -> User:
    statement = select(User, Crew, ObjectStorage).select_from(User).where(User.id == user_id).join(Crew).join(ObjectStorage, isouter=True).join(UserPrivacy, isouter=True).join(Authority, isouter=True)
    user = session.exec(statement).one()

    logging.debug(f"found user: {user}")
    
    return user

async def modify_user(session: SessionDep, query: ModifyUserQuery) -> User:
    statement = select(User).where(User.id == query.user_id)
    user = session.exec(statement).one()


    logging.debug(f"found user: {user}")

    user_data = user.model_dump(exclude_unset=True)
    extra_data = {
        "image_id": query.profile_image_id,
        "instagram_id": query.instagram_id
    }

    user.sqlmodel_update(user_data, update=extra_data)
    session.add(user)
    await session.commit()

    logging.debug(f"modified user: {user}")
    
    return user