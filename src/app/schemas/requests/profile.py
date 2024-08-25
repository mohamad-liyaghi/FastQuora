from pydantic import BaseModel, EmailStr


class UserProfileRequest(BaseModel):
    email: EmailStr
    nickname: str
    biography: str
