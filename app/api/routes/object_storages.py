from fastapi import APIRouter, Depends, Response, UploadFile

from app.api.deps import SessionDep, get_current_user
from app.api.routes.schemas import ModifyUserPrivacyRequest, SearchUserPrivacyResponse
from app.consts import Bucket
import app.core.converter as converter
import app.core.proxy as proxy

router = APIRouter()

@router.post("/object-storage/{bucket}")
async def modify_user_privacy(session: SessionDep, bucket: Bucket, file: UploadFile, my_user_id=Depends(get_current_user)):
    await proxy.upload_file(session, bucket, file, my_user_id)
    return Response(status_code=200)