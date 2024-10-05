from typing import Optional

from pydantic import BaseModel


# TODO: fields validation

class SearchCrewsAllResponse(BaseModel):
    crew_id: int = 0
    name: str
    contents: Optional[str]
    sns: Optional[str]
    region: Optional[str]
    image_uri: Optional[str]

class SignInRequest(BaseModel):
    kakao_auth_code: str

class SignUpRequest(BaseModel):
    user_name: str
    crew_id: int
    instagram_id: Optional[str]

class SignUpResponse(BaseModel):
    name: str

class SignInResponse(BaseModel):
    is_member: bool
    access_token: str

class SearchMyDetailResponse(BaseModel):
    user_id: int
    user_name: str
    crew_name: str
    age_range: Optional[str]
    birthday: Optional[str]
    gender: Optional[str]
    profile_image_uri: Optional[str]
    is_admin: bool
    is_manager: bool
    yellow_card_qty: int
    instagram_uri: Optional[str]
    is_gender_public: bool
    is_birthday_public: bool
    is_instagram_id_public: bool

class ModifyUserRequest(BaseModel):
    profile_image_id: Optional[int]
    instagram_id: Optional[str]

class ModifyUserResponse(BaseModel):
    userName: str

class ModifyUserPrivacyRequest(BaseModel):
    isGenderPublic: bool
    isBirthdayPublic: bool
    isInstagramIdPublic: bool

class SearchUserPrivacyResponse(BaseModel):
    user_id: int
    isGenderPublic: bool
    isBirthdayPublic: bool
    isInstagramIdPublic: bool

class UploadFileResponse(BaseModel):
    file_id: int
    file_uri: str
    user_id: int

class SearchMarathonsRequest(BaseModel):
    locations: Optional[list[str]]
    courses: Optional[list[str]]

class SearchMarathonsResponse(BaseModel):
    marathon_id: int
    title: Optional[str]
    schedule: Optional[str]
    venue: Optional[str]
    course: Optional[str]
    is_bookmarking: bool