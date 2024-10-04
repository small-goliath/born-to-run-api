from fastapi import APIRouter, Depends
from fastapi.responses import RedirectResponse

from app.api.deps import CurrentUserId, SessionDep, get_current_user
from app.api.routes.schemas import SignInRequest, SignInResponse, SignUpRequest, SignUpResponse
import app.core.proxy as proxy
import app.core.converter as converter

router = APIRouter()

@router.get("/kakao/auth-code")
async def get_kakao_auth_code() -> RedirectResponse:
    redirect_uri = await proxy.get_kakao_auth_code()
    return RedirectResponse(url=redirect_uri)
    

@router.post("/sign-in")
async def sign_in(request: SignInRequest) -> SignInResponse:
    sign_in_result = await proxy.sign_in(request)
    return converter.to_signInResponse(sign_in_result)
    
@router.post("/sign-up")
async def sign_up(session: SessionDep, request: SignUpRequest, my_user_id=Depends(get_current_user)) -> SignUpResponse:
    sign_up_result = await proxy.sign_up(session, request, my_user_id)
    return converter.to_signUpResponse(sign_up_result)
    