from app.api.deps import SessionDep
from app.core.config import settings
from app.models import SignInCommand, SignInResult, SignUpCommand, SignUpResult
import app.core.converter as converter
import app.core.converter as converter
import app.infrastructer.join_gateway as join_gateway

async def get_kakao_auth_code() -> str:
    return settings.KAKAO_AUTH_CODE_URI

async def sign_in(command: SignInCommand) -> SignInResult:
    sign_in_response = await join_gateway.sign_in(converter.signInCommand_to_oautn2SignInRequest(command))
    token_response = await join_gateway.get_token(sign_in_response.kakao_id)

    return converter.oautn2TokenResponse_to_signInResult(sign_in_response, token_response)

async def sign_up(session: SessionDep, command: SignUpCommand) -> SignUpResult:
    return await join_gateway.sign_up(session, converter.signUpCommand_to_signUpQuery(command))