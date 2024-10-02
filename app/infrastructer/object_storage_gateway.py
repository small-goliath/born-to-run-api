import io
import uuid
from fastapi import HTTPException
from sqlmodel import select

from app.api.deps import SessionDep
from app.core.config import settings
from app.models import ModifyUserPrivacyQuery, ObjectStorage, UploadFileQuery, UserPrivacy
import logging
from minio import Minio, S3Error

minio_client = Minio(
            "124.58.209.123:9000",  # Minio 서버의 엔드포인트
            access_key="c4XAIlNhnNEcuUZud5WT",  # 액세스 키
            secret_key="83fz49gfdSQjPDCok7jdTaOCwuujuMLTeVccJr5Q",  # 비밀 키
            secure=False
        )

async def upload_file(session: SessionDep, query: UploadFileQuery) -> str:
    # TODO: upload
    logging.debug(f"Try to upload file name: {query.file.filename}")

    try:
        extension = query.file.filename.split('.')[-1]
        uploaded_file_name = f"{uuid.uuid4()}.{extension}"
        logging.info(f"{query.bucket.value}에 {uploaded_file_name} ({query.file.size}bytes) 을 저장합니다.")

        file_data = await query.file.read()
        file_size = len(file_data)  # 바이트

        minio_client.put_object(
            bucket_name=query.bucket.value,
            object_name=uploaded_file_name,
            data=io.BytesIO(file_data),
            length=file_size,
            part_size=5 * 1024 * 1024,
            content_type=query.file.content_type
        )

        cdn_uri = f"{settings.CDN_HOST}/{query.bucket.value}/{uploaded_file_name}"
        uploaded = ObjectStorage(user_id=query.user_id, file_uri=cdn_uri)

        session.add(uploaded)
        session.commit()
        logging.debug(f"SUCCESS to upload file: {uploaded}")

        return uploaded_file_name
    except S3Error as e:
        raise HTTPException(status_code=500, detail=f"MinIO 서버 오류: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"파일 업로드 오류: {str(e)}")