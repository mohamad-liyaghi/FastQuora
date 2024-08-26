from fastapi.routing import APIRouter
from fastapi import Depends, status
from core.factory import Factory
from uuid import UUID
from app.controllers import QuestionController
from app.models import User
from core.dependencies import AuthenticationRequired
from app.schemas.requests.question import QuestionCreateRequest, QuestionUpdateRequest
from app.schemas.responses.question import (
    QuestionCreateResponse,
    QuestionRetrieveResponse,
    QuestionUpdateResponse,
)


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


@router.get("/{question_uuid}", status_code=status.HTTP_200_OK)
async def retrieve_question(
    question_uuid: UUID,
    question_controller: QuestionController = Depends(Factory().get_question_controller),
    _: User = Depends(AuthenticationRequired()),
) -> QuestionRetrieveResponse:
    """Retrieve a question by its uuid."""
    return await question_controller.retrieve_by_uuid(uuid=question_uuid)


@router.put("/{question_uuid}", status_code=status.HTTP_200_OK)
async def update_question(
    question_uuid: UUID,
    request: QuestionUpdateRequest,
    question_controller: QuestionController = Depends(Factory().get_question_controller),
    user: User = Depends(AuthenticationRequired()),
) -> QuestionUpdateResponse:
    """Update a question by its uuid."""
    data = request.model_dump()
    return await question_controller.update_question(uuid=question_uuid, data=data, user_id=user.id)


@router.delete("/{question_uuid}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_question(
    question_uuid: UUID,
    question_controller: QuestionController = Depends(Factory().get_question_controller),
    user: User = Depends(AuthenticationRequired()),
) -> None:
    """Delete a question by its uuid."""
    await question_controller.delete_question(uuid=question_uuid, user_id=user.id)
    return
