from pydantic import BaseModel, EmailStr


class UserRegisterRequest(BaseModel):
    email: EmailStr
    nickname: str
    biography: str
    password: str


class UserLoginRequest(BaseModel):
    email: EmailStr
    password: str
