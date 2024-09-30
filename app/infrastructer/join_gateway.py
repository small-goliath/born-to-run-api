from dataclasses import asdict
import logging

from fastapi import HTTPException
from sqlmodel import select
from app.api.deps import SessionDep
from app.core.config import settings
import httpx
from app.infrastructer.models import SignUpQuery
from app.infrastructer.schemas import OAutn2SignInRequest, OAutn2SignInResponse, OAutn2TokenRequest, OAutn2TokenResponse
from app.models import SignUpResult, User

async def sign_in(request: OAutn2SignInRequest) -> OAutn2SignInResponse:
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"{settings.OAUTH2_HOST}{settings.OAUTH2_SIGN_IN_PATH}",
            params={"code": request.kakao_auth_code}
        )
    
        if response.status_code != 200:
            raise HTTPException(
                status_code=response.status_code,
                detail=f"로그인 오류. statusCode: {response.status_code}"
            )
    
        response_json = response.json()
        return OAutn2SignInResponse(is_member=response_json.get("isMember"), kakao_id=response_json.get("kakaoId"))

async def get_token(kakao_user_id: str) -> OAutn2TokenResponse:
        request = OAutn2TokenRequest(grant_type="client_credentials")
        auth = httpx.BasicAuth(username=kakao_user_id, password=kakao_user_id)
        
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{settings.OAUTH2_HOST}{settings.OAUTH2_AUTH_TOKEN_PATH}",
                auth=auth,
                headers={
                    "Content-Type": "application/x-www-form-urlencoded"
                },
                data=asdict(request)
            )
            
            if response.status_code != 200:
                raise HTTPException(
                    status_code=response.status_code,
                    detail=f"우리 토큰 요청 오류. statusCode: {response.status_code}, response: {response.text}"
                )
            
            response_json = response.json()
            return OAutn2TokenResponse(access_token=response_json.get("access_token"))
        
async def sign_up(session: SessionDep, request: SignUpQuery) -> SignUpResult:
    statement = select(User).where(User.id == request.my_user_id)
    user = session.exec(statement).one()

    logging.debug(f"found user: {user}")

    user_data = user.model_dump(exclude_unset=True)
    extra_data = {
        "name": request.user_name,
        "crew_id": request.crew_id,
        "instagram_id": request.instagram_id
    }

    user.sqlmodel_update(user_data, update=extra_data)
    session.add(user)
    session.commit()

    return SignUpResult(name=user.name)