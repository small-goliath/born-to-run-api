from dataclasses import dataclass

from pydantic import BaseModel


class OAutn2SignInRequest(BaseModel):
    kakao_auth_code: str
    
class OAutn2SignInResponse(BaseModel):
    is_member: bool
    kakao_id: str

@dataclass
class OAutn2TokenRequest:
    grant_type: str
    
class OAutn2TokenResponse(BaseModel):
    access_token: str