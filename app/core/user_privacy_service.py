import app.core.converter as converter
import app.infrastructer.user_privacy_gateway as user_privacy_gateway
from app.api.deps import SessionDep
from app.models import ModifyUserPrivacyCommand, UserPrivacyGlobal


async def modify_user_privacy(session: SessionDep, command: ModifyUserPrivacyCommand):
    query = converter.to_modifyUserPrivacyQuery(command)
    modified = await user_privacy_gateway.modify_user_privacy(session, query)

async def search_user_privacy(session: SessionDep, my_user_id: int) -> UserPrivacyGlobal:
    searched = await user_privacy_gateway.search_user_privacy(session, my_user_id)
    return converter.to_userPrivacyGlobal(searched)