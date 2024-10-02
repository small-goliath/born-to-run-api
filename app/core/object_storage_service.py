from app.api.deps import SessionDep
from app.models import ModifyUserPrivacyCommand, UploadFileCommand, UserPrivacyGlobal
import app.infrastructer.object_storage_gateway as object_storage_gateway
import app.core.converter as converter

async def upload_file(session: SessionDep, command: UploadFileCommand):
    query = converter.to_uploadFileQuery(command)
    modified = await object_storage_gateway.upload_file(session, query)