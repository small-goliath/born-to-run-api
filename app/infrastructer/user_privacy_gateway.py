import logging

from sqlmodel import select

from app.api.deps import SessionDep
from app.models import ModifyUserPrivacyQuery, UserPrivacy


async def modify_user_privacy(session: SessionDep, query: ModifyUserPrivacyQuery):
    statement = select(UserPrivacy).where(UserPrivacy.user_id == query.my_user_id)
    user = session.exec(statement).one()

    logging.debug(f"found user privacy: {user}")

    user_data = user.model_dump(exclude_unset=True)
    extra_data = {
        "is_gender_public": query.is_gender_public,
        "is_birthday_public": query.is_birthday_public,
        "is_instagram_id_public": query.is_instagram_id_public
    }

    user.sqlmodel_update(user_data, update=extra_data)
    session.add(user)
    await session.commit()

    logging.debug(f"modified user privacy: {user}")

async def search_user_privacy(session: SessionDep, my_user_id: int) -> UserPrivacy:
    statement = select(UserPrivacy).where(UserPrivacy.user_id == my_user_id)
    user_privacy = session.exec(statement).one()

    logging.debug(f"found user privacy: {user_privacy}")
    
    return user_privacy