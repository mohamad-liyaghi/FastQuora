from fastapi.routing import APIRouter
from fastapi import Depends, status
from core.factory import Factory
from app.controllers import AnswerController, QuestionController
from app.schemas.requests.answer import AnswerCreateRequest
from app.schemas.responses.answer import AnswerCreateResponse
from app.models import User
from core.dependencies import AuthenticationRequired

router = APIRouter(
    tags=["Answer"],
)


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_answer(
    request: AnswerCreateRequest,
    answer_controller: AnswerController = Depends(Factory().get_answer_controller),
    question_controller: QuestionController = Depends(Factory().get_question_controller),
    user: User = Depends(AuthenticationRequired()),
) -> AnswerCreateResponse:
    """Create a new answer."""
    data = request.model_dump()
    data["user_id"] = user.id
    question_uuid = data.pop("question_uuid")
    return await answer_controller.create_answer(
        question_controller=question_controller, question_uuid=question_uuid, data=data
    )
