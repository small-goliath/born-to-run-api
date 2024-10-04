import io
import logging
import uuid

from fastapi import HTTPException
from minio import Minio, S3Error
from sqlmodel import select

from app.api.deps import SessionDep
from app.core.config import settings
from app.models import Authority, DropFileQuery, ObjectStorage, UploadFileQuery, User

minio_client = Minio(
            settings.MINIO_ENDPOINT,
            access_key=settings.MINIO_ACCESS_KEY,
            secret_key=settings.MINIO_SECRET_KEY,
            secure=False
        )

async def upload_file(session: SessionDep, query: UploadFileQuery) -> ObjectStorage:
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

        return uploaded
    except S3Error as e:
        raise HTTPException(status_code=500, detail=f"MinIO 서버 오류: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"파일 업로드 오류: {str(e)}")
    
async def drop_file(session: SessionDep, query: DropFileQuery):
    try:
        logging.debug(f"Try to drop file id: {query.file_id}")

        statement = select(ObjectStorage, User).select_from(ObjectStorage).join(User, onclause=ObjectStorage.user_id == User.id).join(Authority, onclause=User.id == Authority.user_id).where(ObjectStorage.file_id == query.file_id)


        results = session.exec(statement).one_or_none()
        logging.debug(f"selected objectStorage row: {results}")

        if results is None:
            raise HTTPException(status_code=404, detail="파일이 존재하지 않습니다.")

        objectStorage = results[0]
        user = results[1]
        authorities = user.authority

        if query.user_id != user.id:
            for authority in authorities:
                if "ADMIN" not in authority.authority:
                    raise HTTPException(status_code=400, detail="관리자 외 본인의 파일만 제거할 수 있습니다.")

        minio_client.remove_object(query.bucket.value, objectStorage.file_uri.split('/')[-1])

        session.delete(objectStorage)
        session.commit()

        logging.debug(f"SUCCESS to drop file: {results}")
    except S3Error as e:
        logging.error(e)
        raise HTTPException(status_code=500, detail=f"MinIO 서버 오류: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"파일 삭제 오류: {str(e)}")