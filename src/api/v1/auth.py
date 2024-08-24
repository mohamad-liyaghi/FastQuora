from fastapi import Depends, status
from fastapi.routing import APIRouter
from core.factory import Factory
from app.schemas.requests.auth import UserRegisterRequest
from app.schemas.responses.auth import UserRegisterResponse
from app.controllers import AuthController


router = APIRouter(
    tags=["Authentication"],
)


@router.post("/register", status_code=status.HTTP_201_CREATED)
async def register_user(
    request: UserRegisterRequest,
    auth_controller: AuthController = Depends(Factory().get_auth_controller),
) -> UserRegisterResponse:
    """Register a new user."""
    return await auth_controller.register(data=request.model_dump())
