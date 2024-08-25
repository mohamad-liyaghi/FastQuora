from pydantic import BaseModel, EmailStr
from datetime import datetime


class UserProfileResponse(BaseModel):
    email: EmailStr
    nickname: str
    biography: str
    date_joined: datetime
