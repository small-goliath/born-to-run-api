from fastapi import APIRouter

import app.core.proxy as proxy

router = APIRouter()

@router.get("/kakao/auth-code")
async def get_kakao_auth_code() -> str:
    return await proxy.get_kakao_auth_code()