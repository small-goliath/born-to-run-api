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