from fastapi import Depends, status, HTTPException, Request
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from uuid import UUID
from app.models import User
from core.factory import Factory
from app.controllers import ProfileController


class AuthenticationRequired:
    """
    Make sure the user is authenticated.
    """

    async def __call__(
        self,
        request: Request,
        token: HTTPAuthorizationCredentials = Depends(HTTPBearer(auto_error=False)),
        user_controller: ProfileController = Depends(Factory().get_profile_controller),
    ) -> User:
        """
        Check if the user is authenticated and return the user
        """
        if not token:
            raise HTTPException(detail="Authentication required", status_code=status.HTTP_403_FORBIDDEN)
        return await user_controller.get_by_uuid(UUID(request.user.uuid))
