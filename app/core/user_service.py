import logging
from app.api.deps import SessionDep
from app.models import CrewGlobal, UserGlobal
import app.infrastructer.user_gateway as user_gateway
import app.core.converter as converter

async def search_user_detail(session: SessionDep, my_user_id: int) -> UserGlobal:
    user = await user_gateway.search_user(session, my_user_id)
    return converter.user_to_userGlobal(user)