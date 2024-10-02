from app.api.deps import SessionDep
from app.models import DropFileCommand, ModifyUserPrivacyCommand, UploadFileCommand, UserPrivacyGlobal
import app.infrastructer.object_storage_gateway as object_storage_gateway
import app.core.converter as converter

async def upload_file(session: SessionDep, command: UploadFileCommand):
    query = converter.to_uploadFileQuery(command)
    await object_storage_gateway.upload_file(session, query)

async def drop_file(session: SessionDep, command: DropFileCommand):
    query = converter.to_dropFileQuery(command)
    await object_storage_gateway.drop_file(session, query)