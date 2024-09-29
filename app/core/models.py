from pydantic import BaseModel, Field
from dataclasses import dataclass

# TODO: Fields validation

@dataclass
class SignInCommand(BaseModel):
    kakao_auth_code: str = Field(..., min_length=100, max_length=100)