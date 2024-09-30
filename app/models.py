from dataclasses import dataclass
from typing import Optional
from pydantic import BaseModel
from sqlmodel import Field, Relationship, SQLModel
from datetime import datetime

from app.api.deps import SessionDep

# TODO: Field setting

class CrewBase(SQLModel):
    crew_id: int = Field(primary_key=True)
    name: str
    contents: Optional[str]
    sns: Optional[str]
    region: Optional[str]

class CrewGlobal(CrewBase):
    image: Optional['ObjectStorage']

class Crew(CrewBase, table=True):
    image_id: Optional[int]  = Field(
        default=0,
        foreign_key="object_storage.file_id",
        nullable=True,
        ondelete="CASCADE"
    )
    image: Optional['ObjectStorage'] = Relationship(back_populates="crewImage")
    is_deleted: bool = False

class ObjectStorageBase(SQLModel):
    file_id: int = Field(primary_key=True)
    user_id: int
    file_uri: str
    upload_at: datetime

class ObjectStorage(ObjectStorageBase, table=True):
    __tablename__ = "object_storage"
    crewImage: Optional[Crew] = Relationship(back_populates="image", cascade_delete=True)
    is_deleted: bool = False

class SignInCommand(BaseModel):
    kakao_auth_code: str

class SignUpCommand(BaseModel):
    my_user_id: int
    user_name: str
    crew_id: int
    instagram_id: Optional[str]

class SignInResult(BaseModel):
    is_member: bool
    access_token: str

class SignUpResult(BaseModel):
    name: str

class UserBase(SQLModel):
    id: int = Field(primary_key=True)
    social_id: str
    age_range: str
    name: str
    crew_id: int
    birthday: str
    gender: str
    instagram_id: str
    last_login_at: datetime
    image_id: int
    yellow_card_qty: int
    
class User(UserBase, table=True):
    is_deleted: bool = False