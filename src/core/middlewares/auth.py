from typing import Optional, Tuple
from jose import JWTError, jwt
from pydantic import BaseModel, Field
from uuid import UUID
from starlette.authentication import AuthenticationBackend
from starlette.middleware.authentication import (
    AuthenticationMiddleware as BaseAuthenticationMiddleware,
)
from starlette.requests import HTTPConnection
from core.settings import settings


class CurrentUser(BaseModel):
    uuid: UUID | str = Field(None, description="User UUID")

    class Config:
        validate_assignment: bool = True


class AuthBackend(AuthenticationBackend):
    async def authenticate(self, conn: HTTPConnection) -> Tuple[bool, Optional[CurrentUser]]:
        current_user = CurrentUser()
        authorization: str = conn.headers.get("Authorization")
        if not authorization:
            return False, current_user

        try:
            scheme, token = authorization.split(" ")
            if scheme.lower() != "bearer":
                return False, current_user
        except ValueError:
            return False, current_user

        if not token:
            return False, current_user

        try:
            payload = jwt.decode(
                token,
                settings.SECRET_KEY,
                algorithms=[settings.JWT_ALGORITHM],
            )
            user_uuid = payload.get("user_uuid")
        except JWTError:
            return False, current_user

        current_user.uuid = user_uuid
        return True, current_user


class AuthenticationMiddleware(BaseAuthenticationMiddleware):
    pass
