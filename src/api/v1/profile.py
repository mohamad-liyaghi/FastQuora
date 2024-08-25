from fastapi.routing import APIRouter
from fastapi import Depends, status
from uuid import UUID
from core.factory import Factory
from app.controllers import ProfileController
from app.schemas.requests.profile import UserProfileRequest
from app.schemas.responses.profile import UserProfileResponse
from core.dependencies import AuthenticationRequired
from app.models import User


router = APIRouter(
    tags=["Profile"],
)


@router.get("/{user_uuid}", status_code=status.HTTP_200_OK)
async def retrieve_profile(
    user_uuid: UUID,
    profile_controller: ProfileController = Depends(Factory().get_profile_controller),
    _: User = Depends(AuthenticationRequired()),
) -> UserProfileResponse:
    """Retrieve a user's information by its uuid."""
    return await profile_controller.get_by_uuid(uuid=user_uuid)


@router.put("/{user_uuid}", status_code=status.HTTP_200_OK)
async def update_profile(
    request: UserProfileRequest,
    user_uuid: UUID,
    profile_controller: ProfileController = Depends(Factory().get_profile_controller),
    current_user: AuthenticationRequired = Depends(AuthenticationRequired()),
) -> UserProfileResponse:
    """Update a user's information by its owner."""
    return await profile_controller.update_user(
        user_uuid=user_uuid, requesting_user=current_user, data=request.model_dump()
    )
