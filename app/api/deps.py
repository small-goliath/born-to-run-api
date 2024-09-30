from collections.abc import Generator
from typing import Annotated

import jwt
from fastapi import Depends, HTTPException, Security, status
from fastapi.security import APIKeyHeader, OAuth2PasswordBearer
from jwt.exceptions import InvalidTokenError
from pydantic import ValidationError
from sqlmodel import Session
from cryptography.hazmat.primitives.serialization import pkcs12
from cryptography.hazmat.backends import default_backend

from app.core.config import settings
from app.core.db import engine
import logging

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

def get_current_user(access_token=Security(APIKeyHeader(name='Authentication'))) -> int:
    try:
        private_key, certificate = load_pkcs12_keystore('../oauth2runacerApi.p12', settings.P12_SECRET_KEY)
        public_key = certificate.public_key()

        payload = jwt.decode(
            jwt=access_token,
            key=public_key,
            algorithms=['RS256'],
            options={"verify_aud": False},
        )

        user_id = payload['id']
    except (InvalidTokenError, ValidationError) as e:
        logging.error(f"Token validation failed: {e}")

        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=str(e),
        )
    
    if not user_id:
        raise HTTPException(status_code=401, detail="로그인이 필요합니다.")
    return user_id


CurrentUserId = Annotated[int, Depends(get_current_user)]