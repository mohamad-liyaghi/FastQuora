from pydantic import BaseModel, EmailStr


class UserRegisterResponse(BaseModel):
    email: EmailStr
    nickname: str
    biography: str
