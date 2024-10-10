from datetime import datetime
from typing import Optional

from fastapi import UploadFile
from pydantic import BaseModel
from sqlmodel import Field, Relationship, SQLModel

from app.consts import Bucket


# TODO: Field setting, index setting

class CrewBase(SQLModel):
    crew_id: int = Field(primary_key=True)
    name: str
    contents: Optional[str]
    sns: Optional[str]
    region: Optional[str]

class CrewGlobal(CrewBase):
    image: Optional['ObjectStorage']

class Crew(CrewBase, table=True):
    image_id: Optional[int] = Field(
        default=0,
        foreign_key="object_storage.file_id"
    )
    image: Optional['ObjectStorage'] = Relationship(back_populates="crew_image", sa_relationship_kwargs=dict(foreign_keys="[Crew.image_id]"))
    user: Optional['User'] = Relationship(back_populates="crew")
    is_deleted: bool = False

class ObjectStorageBase(SQLModel):
    file_id: int = Field(primary_key=True)
    file_uri: str
    upload_at: datetime = Field(default_factory=datetime.now)

class ObjectStorage(ObjectStorageBase, table=True):
    __tablename__ = "object_storage"
    crew_image: Optional[Crew] = Relationship(back_populates="image")
    user_image: Optional['User'] = Relationship(back_populates="image", sa_relationship_kwargs=dict(foreign_keys="[User.image_id]"))
    user_id: int = Field(foreign_key="user.id")
    user: 'User' = Relationship(back_populates="object_storages", sa_relationship_kwargs=dict(foreign_keys="[ObjectStorage.user_id]"))
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
      foreign_key="user.id"
    )
  user: 'User' = Relationship(back_populates="user_privacy", sa_relationship_kwargs=dict(foreign_keys="[UserPrivacy.user_id]"))
    
class AuthorityBase(SQLModel):
    id: int = Field(primary_key=True)
    authority: str

class Authority(AuthorityBase, table=True):
    user_id: int = Field(
        default=0,
        foreign_key="user.id"
    )
    user: 'User' = Relationship(back_populates="authority", sa_relationship_kwargs=dict(foreign_keys="[Authority.user_id]"))

class User(UserBase, table=True):
    crew_id: Optional[int] = Field(
        default=0,
        foreign_key="crew.crew_id"
    )
    image_id: Optional[int] = Field(
        default=0,
        foreign_key="object_storage.file_id"
    )
    crew: Crew = Relationship(back_populates="user", sa_relationship_kwargs=dict(foreign_keys="[User.crew_id]"))
    image: Optional[ObjectStorage] = Relationship(back_populates="user_image", sa_relationship_kwargs=dict(foreign_keys="[User.image_id]"))
    user_privacy: UserPrivacy = Relationship(back_populates="user")
    authority: list[Authority] = Relationship(back_populates="user")
    object_storages: Optional[list[ObjectStorage]] = Relationship(back_populates="user", sa_relationship_kwargs=dict(foreign_keys="[ObjectStorage.user_id]"))
    marathon_bookmarks: Optional[list['MarathonBookmark']] = Relationship(back_populates="user", sa_relationship_kwargs=dict(foreign_keys="[MarathonBookmark.user_id]"))
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

class SignUpQuery(BaseModel):
    my_user_id: int
    user_name: str
    crew_id: int
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

class UploadFileGlobal(BaseModel):
    file_id: int
    file_uri: str
    user_id: int
    

class DropFileCommand(BaseModel):
    user_id: int
    file_id: int
    bucket: Bucket

class DropFileQuery(BaseModel):
    user_id: int
    file_id: int
    bucket: Bucket

class SearchMarathonsCommand(BaseModel):
    my_user_id: int
    locations: Optional[list[str]]
    courses: Optional[list[str]]

class MarathonGlobal(BaseModel):
    id: int
    title: Optional[str]
    owner: Optional[str]
    email: Optional[str]
    schedule: Optional[str]
    contact: Optional[str]
    course: Optional[str]
    location: Optional[str]
    venue: Optional[str]
    host: Optional[str]
    duration: Optional[str]
    homepage: Optional[str]
    venue_detail: Optional[str]
    remark: Optional[str]
    registered_at: datetime
    is_my_bookmark: bool

class SearchMarathonsQuery(BaseModel):
    my_user_id: int
    locations: Optional[list[str]]
    courses: Optional[list[str]]

class MarathonBase(SQLModel):
    id: int = Field(primary_key=True)
    title: str
    owner: str
    email: str
    schedule: str
    contact: str
    course: str
    location: str
    venue: str
    host: str
    duration: str
    homepage: str
    venue_detail: str
    remark: str
    registered_at: datetime
    is_deleted: bool

class Marathon(MarathonBase, table=True):
    marathon_bookmarks: list['MarathonBookmark'] = Relationship(back_populates="marathon")

class MarathonBookmarkBase(SQLModel):
    bookmark_id: int = Field(primary_key=True)
    registered_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)
    is_deleted: bool = False

class MarathonBookmark(MarathonBookmarkBase, table=True):
    __tablename__ = "marathon_bookmark"
    user_id: int = Field(
        default=0,
        foreign_key="user.id"
    )
    marathon_id: int = Field(
        default=0,
        foreign_key="marathon.id"
    )
    marathon: Marathon = Relationship(back_populates="marathon_bookmarks", sa_relationship_kwargs=dict(foreign_keys="[MarathonBookmark.marathon_id]"))
    user: User = Relationship(back_populates="marathon_bookmarks", sa_relationship_kwargs=dict(foreign_keys="[MarathonBookmark.user_id]"))

class SearchMarathonDetailCommand(BaseModel):
    my_user_id: int
    marathon_id: int

class SearchMarathonDetailQuery(BaseModel):
    my_user_id: int
    marathon_id: int

class BookmarkMarathonCommand(BaseModel):
    my_user_id: int
    marathon_id: int

class BookmarkMarathonQuery(BaseModel):
    my_user_id: int
    marathon_id: int