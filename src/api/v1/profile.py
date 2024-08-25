from fastapi.routing import APIRouter
from fastapi import Depends, status
from uuid import UUID
from core.factory import Factory
from app.controllers import ProfileController
from app.schemas.responses.profile import UserProfileResponse


router = APIRouter(
    tags=["Profile"],
)


@router.get("/{user_uuid}", status_code=status.HTTP_200_OK)
async def retrieve_profile(
    user_uuid: UUID,
    profile_controller: ProfileController = Depends(Factory().get_profile_controller),
) -> UserProfileResponse:
    """Retrieve a user's information by its uuid."""
    return await profile_controller.get_by_uuid(uuid=user_uuid)
