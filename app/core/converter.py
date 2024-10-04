from app.api.deps import CurrentUserId, SessionDep
from app.infrastructer.models import SignUpQuery
from app.infrastructer.schemas import OAutn2SignInRequest, OAutn2SignInResponse, OAutn2TokenResponse
from app.models import Crew, CrewGlobal, DropFileCommand, DropFileQuery, ModifyUserCommand, ModifyUserPrivacyCommand, ModifyUserQuery, SignInCommand, SignInResult, SignUpCommand, SignUpResult, UploadFileCommand, UploadFileQuery, User, UserGlobal, UserPrivacy, UserPrivacyGlobal
from app.api.routes.schemas import ModifyUserRequest, SearchCrewsAllResponse, SearchMyDetailResponse, SearchUserPrivacyResponse, SignInRequest, SignInResponse, SignUpRequest, SignUpResponse

# TODO: 등록된 크루가 굉장히 많아지면 async
def to_crewGlobal(source: list[Crew]) -> list[CrewGlobal]:
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

def to_searchCrewsAllResponse(source: list[CrewGlobal]) -> list[SearchCrewsAllResponse]:
    result = []
    for s in source:
        result.append(SearchCrewsAllResponse(crew_id=s.crew_id,
        name=s.name,
        contents=s.contents,
        sns=s.sns,
        region=s.region,
        image_uri=s.image.file_uri if s.image else None))
    return result

def to_signInCommand(source: SignInRequest) -> SignInCommand:
    return SignInCommand(kakao_auth_code=source.kakao_auth_code)

def to_oautn2SignInRequest(source: SignInCommand) -> OAutn2SignInRequest:
    return OAutn2SignInRequest(kakao_auth_code=source.kakao_auth_code)

def to_signInResult(sign_in_source: OAutn2SignInResponse, token_source: OAutn2TokenResponse) -> SignInResult:
    return SignInResult(is_member=sign_in_source.is_member, access_token=token_source.access_token)

def to_signInResponse(source: SignInResult) -> SignInResponse:
    return SignInResponse(is_member=source.is_member, access_token=source.access_token)

def to_signUpCommand(source: SignUpRequest, my_user_id: int) -> SignUpCommand:
    return SignUpCommand(user_name=source.user_name, crew_id=source.crew_id, instagram_id=source.instagram_id, my_user_id=my_user_id)

def to_signUpQuery(source: SignUpCommand) -> SignUpQuery:
    return SignUpQuery(user_name=source.user_name, crew_id=source.crew_id, instagram_id=source.instagram_id, my_user_id=source.my_user_id)

def to_signUpResponse(source: SignUpResult) -> SignUpResponse:
    return SignUpResponse(name=source.name)

def to_userGlobal(source: User) -> UserGlobal:
    source = source[0]
    return UserGlobal(id=source.id,
                      social_id=source.social_id,
                      age_range=source.age_range,
                      name=source.name,
                      birthday=source.birthday,
                      gender=source.gender,
                      instagram_id=source.instagram_id,
                      last_login_at=source.last_login_at,
                      yellow_card_qty=source.yellow_card_qty,
                      crew=source.crew,
                      image_uri=source.image.file_uri if source.image else None,
                      is_admin=True if "ADMIN" in source.authority else False,
                      is_manager=True if "MANAGER" in source.authority else False,
                      is_gender_public=source.user_privacy.is_gender_public,
                      is_birthday_public=source.user_privacy.is_birthday_public,
                      is_instagram_id_public=source.user_privacy.is_instagram_id_public)

def to_searchMyDetailResponse(source: UserGlobal) -> SearchMyDetailResponse:
    return SearchMyDetailResponse(user_id=source.id,
                                  user_name=source.name,
                                  crew_name=source.crew.name,
                                  age_range=source.age_range,
                                  birthday=source.birthday,
                                  gender=source.gender,
                                  profile_image_uri=source.image_uri,
                                  is_admin=source.is_admin,
                                  is_manager=source.is_manager,
                                  yellow_card_qty=source.yellow_card_qty,
                                  instagram_uri=f"https://www.instagram.com/{source.instagram_id}",
                                  is_gender_public=source.is_gender_public,
                                  is_birthday_public=source.is_birthday_public,
                                  is_instagram_id_public=source.is_instagram_id_public)

def to_modifyUserCommand(source: ModifyUserRequest, user_id: int) -> ModifyUserCommand:
    return ModifyUserCommand(user_id=user_id,
                             profile_image_id=source.profile_image_id,
                             instagram_id=source.instagram_id)

def to_modifyUserQuery(source: ModifyUserCommand, user_id: int) -> ModifyUserQuery:
    return ModifyUserCommand(user_id=user_id,
                             profile_image_id=source.profile_image_id,
                             instagram_id=source.instagram_id)

def to_ModifyUserPrivacyCommand(source: ModifyUserRequest, user_id: int) -> ModifyUserPrivacyCommand:
    return ModifyUserPrivacyCommand(my_user_id=user_id,
                                    is_gender_public=source.is_gender_public,
                                    is_birthday_public=source.is_birthday_public,
                                    is_instagram_id_public=source.is_instagram_id_public)

def to_modifyUserPrivacyQuery(source: ModifyUserPrivacyCommand):
    return ModifyUserPrivacyCommand(my_user_id=source.my_user_id,
                                    is_gender_public=source.is_gender_public,
                                    is_birthday_public=source.is_birthday_public,
                                    is_instagram_id_public=source.is_instagram_id_public)

def to_userPrivacyGlobal(source: UserPrivacy) -> UserPrivacyGlobal:
    return UserPrivacyGlobal(my_user_id=source.user_id,
                                    is_gender_public=source.is_gender_public,
                                    is_birthday_public=source.is_birthday_public,
                                    is_instagram_id_public=source.is_instagram_id_public)

def to_searchUserPrivacyResponse(source: UserPrivacyGlobal) -> SearchUserPrivacyResponse:
    return SearchUserPrivacyResponse(user_id=source.user_id,
                                    is_gender_public=source.is_gender_public,
                                    is_birthday_public=source.is_birthday_public,
                                    is_instagram_id_public=source.is_instagram_id_public)

def to_uploadFileQuery(source: UploadFileCommand) -> UploadFileQuery:
    return UploadFileQuery(user_id=source.user_id,
                           bucket=source.bucket,
                           file=source.file)

def to_dropFileQuery(source: DropFileCommand) -> DropFileQuery:
    return DropFileQuery(user_id=source.user_id,
                        bucket=source.bucket,
                        file_id=source.file_id)