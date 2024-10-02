from dataclasses import dataclass
from typing import Optional
from fastapi import UploadFile
from pydantic import BaseModel
from sqlmodel import Field, Relationship, SQLModel
from datetime import datetime

from app.api.deps import SessionDep
from app.consts import Bucket

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
    image: Optional['ObjectStorage'] = Relationship(back_populates="crew_image")
    user: Optional['User'] = Relationship(back_populates="crew")
    is_deleted: bool = False

class ObjectStorageBase(SQLModel):
    file_id: int = Field(primary_key=True)
    user_id: int
    file_uri: str
    upload_at: datetime = Field(default_factory=datetime.now)

class ObjectStorage(ObjectStorageBase, table=True):
    __tablename__ = "object_storage"
    crew_image: Optional[Crew] = Relationship(back_populates="image", cascade_delete=True)
    user_image: Optional['User'] = Relationship(back_populates="image", cascade_delete=True)
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
    age_range: Optional[str]
    name: Optional[str]
    birthday: Optional[str]
    gender: Optional[str]
    instagram_id: Optional[str]
    last_login_at: datetime
    yellow_card_qty: int

class UserPrivacyBase(SQLModel):
  privacy_id: int = Field(primary_key=True)
  is_gender_public: bool
  is_birthday_public: bool
  is_instagram_id_public: bool

class UserPrivacy(UserPrivacyBase, table=True):
  __tablename__ = "user_privacy"
  user_id: int = Field(
        default=0,
        foreign_key="user.id",
        nullable=True,
        ondelete="CASCADE"
    )
  user: 'User' = Relationship(back_populates="user_privacy")
    
class AuthorityBase(SQLModel):
    id: int = Field(primary_key=True)
    authority: str

class Authority(AuthorityBase, table=True):
    user_id: int = Field(
        default=0,
        foreign_key="user.id",
        nullable=True,
        ondelete="CASCADE"
    )
    user: 'User' = Relationship(back_populates="authority")

class User(UserBase, table=True):
    crew_id: int = Field(
        default=0,
        foreign_key="crew.crew_id",
        nullable=True,
        ondelete="CASCADE"
    )
    image_id: Optional[int] = Field(
        default=0,
        foreign_key="object_storage.file_id",
        nullable=True,
        ondelete="CASCADE"
    )
    crew: Crew = Relationship(back_populates="user")
    image: Optional[ObjectStorage] = Relationship(back_populates="user_image")
    user_privacy: UserPrivacy = Relationship(back_populates="user")
    authority: Authority = Relationship(back_populates="user")
    is_deleted: bool = False

class UserGlobal(UserBase):
    crew: Crew
    image_uri: Optional[str]
    is_manager: bool
    is_admin: bool
    is_gender_public: bool
    is_birthday_public: bool
    is_instagram_id_public: bool

class ModifyUserCommand(BaseModel):
    user_id: int
    profile_image_id: Optional[int]
    instagram_id: Optional[str]

class ModifyUserQuery(BaseModel):
    user_id: int
    profile_image_id: Optional[int]
    instagram_id: Optional[str]

class ModifyUserPrivacyCommand(BaseModel):
    my_user_id: int
    isGenderPublic: bool
    isBirthdayPublic: bool
    isInstagramIdPublic: bool

class UserPrivacyGlobal(BaseModel):
    user_id: int
    is_gender_public: bool
    is_birthday_public: bool
    is_instagram_id_public: bool

class ModifyUserPrivacyQuery(BaseModel):
    user_id: int
    is_gender_public: bool
    is_birthday_public: bool
    is_instagram_id_public: bool

class UploadFileCommand(BaseModel):
    user_id: int
    file: UploadFile
    bucket: Bucket

class UploadFileQuery(BaseModel):
    user_id: int
    file: UploadFile
    bucket: Bucket