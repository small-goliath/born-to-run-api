import logging
from collections.abc import Generator
from typing import Annotated

import re
import jwt
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.serialization import pkcs12
from fastapi import Depends, HTTPException, Request, Security, status
from fastapi.security import APIKeyHeader, OAuth2PasswordBearer
from jwt.exceptions import InvalidTokenError
from pydantic import ValidationError
from sqlmodel import Session

from app.core.config import settings
from app.core.db import engine

reusable_oauth2 = OAuth2PasswordBearer(
    tokenUrl=f"{settings.API_V1_STR}/login/access-token"
)


def get_db() -> Generator[Session, None, None]:
    with Session(engine) as session:
        yield session


SessionDep = Annotated[Session, Depends(get_db)]
TokenDep = Annotated[str, Depends(reusable_oauth2)]

def load_pkcs12_keystore(pkcs12_file: str, password: str):
    with open(pkcs12_file, 'rb') as f:
        pkcs12_data = f.read()

    # PKCS12에서 키와 인증서 가져오기
    private_key, certificate, additional_certificates = pkcs12.load_key_and_certificates(
        pkcs12_data, password.encode(), backend=default_backend()
    )

    return private_key, certificate

REQUIRED_LOGIN_APIS: dict[str, list[str]] = {
        "GET": ["/api/v1/users/my", "/api/v1/privacy/user"],
        "POST": ["/api/v1/join/sign-up", "/api/v1/token", "/api/v1/object_storages/{bucket}", "/api/v1/marathons/bookmark/{marathon_id}"],
        "PUT": ["/api/v1/users/my", "/api/v1/privacy/user"],
        "DELETE": ["/api/v1/object_storages/{bucket}/{file_id}", "/api/v1/marathons/bookmark/{marathon_id}"]
}

def path_matches(pattern: str, path: str) -> bool:
    # 정규식으로 경로 변수에 해당하는 부분을 모든 문자열 패턴으로 치환
    regex_pattern = re.sub(r"\{[^\}]+\}", r"[^/]+", pattern)
    return re.match(f"^{regex_pattern}$", path) is not None

def get_current_user(request: Request,
                     access_token=Security(APIKeyHeader(name='Authentication', auto_error=False))) -> int:
    try:
        private_key, certificate = load_pkcs12_keystore('../oauth2runacerApi.p12', settings.P12_SECRET_KEY)
        public_key = certificate.public_key()

        payload = None
        if access_token is not None:
            payload = jwt.decode(
                jwt=access_token,
                key=public_key,
                algorithms=['RS256'],
                options={"verify_aud": False},
            )

        user_id = -1 if payload is None else payload['id']
    except (InvalidTokenError, ValidationError) as e:
        if request.url.path in REQUIRED_LOGIN_APIS.get(request.method):
            logging.error(f"Token validation failed: {e}")

            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=str(e),
            )
        
        return -1

    method = request.method
    path = request.url.path
    required_login_paths = REQUIRED_LOGIN_APIS.get(method, [])

    for required_path in required_login_paths:
        if path_matches(required_path, path) and user_id == -1:
            raise HTTPException(status_code=401, detail="로그인이 필요합니다.")
    
    return user_id


CurrentUserId = Annotated[int, Depends(get_current_user)]