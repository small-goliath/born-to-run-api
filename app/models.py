from typing import Optional
from sqlmodel import Field, Relationship, SQLModel
from datetime import datetime

# TODO: Field setting
# email: EmailStr = Field(unique=True, index=True, max_length=255)
# is_active: bool = True
# is_superuser: bool = False
# full_name: str | None = Field(default=None, max_length=255)

class CrewBase(SQLModel):
    crew_id: int = Field(primary_key=True)
    name: str
    contents: Optional[str]
    sns: Optional[str]
    region: Optional[str]

class CrewGlobal(CrewBase):
    image: Optional['ObjectStorage']

class SearchCrewsAllResponse(CrewBase):
    image_uri: Optional[str]

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

class UserBase(SQLModel):
    id: int = Field(primary_key=True)
    sociald: str
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

class TokenPayload(SQLModel):
    sub: str | None = None