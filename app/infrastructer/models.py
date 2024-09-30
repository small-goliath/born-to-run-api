from typing import Optional
from pydantic import BaseModel

from app.api.deps import CurrentUserId

class SignUpQuery(BaseModel):
    my_user_id: int
    user_name: str
    crew_id: int
    instagram_id: Optional[str]