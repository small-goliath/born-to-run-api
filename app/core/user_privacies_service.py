from app.api.deps import SessionDep
from app.models import ModifyUserPrivacyCommand, UserPrivacyGlobal
import app.infrastructer.user_privacies_gateway as user_privacies_gateway
import app.core.converter as converter

async def modify_user_privacy(session: SessionDep, command: ModifyUserPrivacyCommand):
    query = converter.to_modifyUserPrivacyQuery(command)
    modified = await user_privacies_gateway.modify_user_privacy(session, query)

async def search_user_privacy(session: SessionDep, my_user_id: int) -> UserPrivacyGlobal:
    searched = await user_privacies_gateway.search_user_privacy(session, my_user_id)
    return converter.to_userPrivacyGlobal(searched)