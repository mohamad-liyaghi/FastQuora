from fastapi.routing import APIRouter
from fastapi import Depends, status
from core.factory import Factory
from app.controllers import QuestionController
from app.models import User
from core.dependencies import AuthenticationRequired
from app.schemas.requests.question import QuestionCreateRequest
from app.schemas.responses.question import QuestionCreateResponse


router = APIRouter(
    tags=["Question"],
)


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_question(
    request: QuestionCreateRequest,
    question_controller: QuestionController = Depends(Factory().get_question_controller),
    user: User = Depends(AuthenticationRequired()),
) -> QuestionCreateResponse:
    """Create a new question."""
    data = request.model_dump()
    data["user_id"] = user.id
    return await question_controller.create(data=data)
