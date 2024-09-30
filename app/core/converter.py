from app.api.deps import CurrentUserId, SessionDep
from app.infrastructer.models import SignUpQuery
from app.infrastructer.schemas import OAutn2SignInRequest, OAutn2SignInResponse, OAutn2TokenResponse
from app.models import Crew, CrewGlobal, SignInCommand, SignInResult, SignUpCommand, SignUpResult
from app.api.routes.schemas import SearchCrewsAllResponse, SignInRequest, SignInResponse, SignUpRequest, SignUpResponse

# TODO: 등록된 크루가 굉장히 많아지면 async
def crew_to_crewGlobal(source: list[Crew]) -> list[CrewGlobal]:
    result = []
    for s in source:
        s = s[0]
        result.append(CrewGlobal(crew_id=s.crew_id,
        name=s.name,
        contents=s.contents,
        sns=s.sns,
        region=s.region,
        image=s.image))
    return result

def crewGlobal_to_searchCrewsAllResponse(source: list[CrewGlobal]) -> list[SearchCrewsAllResponse]:
    result = []
    for s in source:
        result.append(SearchCrewsAllResponse(crew_id=s.crew_id,
        name=s.name,
        contents=s.contents,
        sns=s.sns,
        region=s.region,
        image_uri=s.image.file_uri if s.image else None))
    return result

def signInRequest_to_signInCommand(source: SignInRequest) -> SignInCommand:
    return SignInCommand(kakao_auth_code=source.kakao_auth_code)

def signInCommand_to_oautn2SignInRequest(source: SignInCommand) -> OAutn2SignInRequest:
    return OAutn2SignInRequest(kakao_auth_code=source.kakao_auth_code)

def oautn2TokenResponse_to_signInResult(sign_in_source: OAutn2SignInResponse, token_source: OAutn2TokenResponse) -> SignInResult:
    return SignInResult(is_member=sign_in_source.is_member, access_token=token_source.access_token)

def signInResult_to_signInResponse(source: SignInResult) -> SignInResponse:
    return SignInResponse(is_member=source.is_member, access_token=source.access_token)

def signUpRequest_to_signUpCommand(source: SignUpRequest, my_user_id: int) -> SignUpCommand:
    return SignUpCommand(user_name=source.user_name, crew_id=source.crew_id, instagram_id=source.instagram_id, my_user_id=my_user_id)

def signUpCommand_to_signUpQuery(source: SignUpCommand) -> SignUpQuery:
    return SignUpQuery(user_name=source.user_name, crew_id=source.crew_id, instagram_id=source.instagram_id, my_user_id=source.my_user_id)

def signUpResult_to_signUpResponse(source: SignUpResult) -> SignUpResponse:
    return SignUpResponse(name=source.name)