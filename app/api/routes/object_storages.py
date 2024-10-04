from fastapi import APIRouter, Depends, Response, UploadFile

from app.api.deps import SessionDep, get_current_user
from app.consts import Bucket
import app.core.converter as converter
import app.core.proxy as proxy

router = APIRouter()

@router.post("/object-storage/{bucket}")
async def upload_file(session: SessionDep, bucket: Bucket, file: UploadFile, my_user_id=Depends(get_current_user)):
    uploaded = await proxy.upload_file(session, bucket, file, my_user_id)
    return converter.to_uploadFileResponse(uploaded)

@router.delete("/object-storage/{bucket}/{file_id}")
async def drop_file(session: SessionDep, bucket: Bucket, file_id: int, my_user_id=Depends(get_current_user)):
    await proxy.drop_file(session, bucket, file_id, my_user_id)
    return Response(status_code=200)