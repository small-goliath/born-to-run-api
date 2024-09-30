import logging
from app.api.deps import SessionDep
from app.models import CrewGlobal, ModifyUserCommand, ModifyUserPrivacyCommand, UserGlobal
import app.infrastructer.user_gateway as user_gateway
import app.core.converter as converter

async def search_user_detail(session: SessionDep, user_id: int) -> UserGlobal:
    user = await user_gateway.search_user(session, user_id)
    return converter.to_userGlobal(user)

async def modify_user(session: SessionDep, command: ModifyUserCommand) -> str:
    query = converter.to_modifyUserQuery(command)
    modified = await user_gateway.modify_user(session, query)
    return modified.name