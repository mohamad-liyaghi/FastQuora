from fastapi.routing import APIRouter
from fastapi import Depends, status
from uuid import UUID
from typing import Optional
from core.factory import Factory
from app.controllers import AnswerController, QuestionController
from app.schemas.requests.answer import (
    AnswerCreateRequest,
    AnswerUpdateRequest,
    AnswerReplyCreateRequest,
)
from app.schemas.responses.answer import (
    AnswerCreateResponse,
    AnswerUpdateResponse,
    AnswerResponse,
)
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


@router.put("/{answer_uuid}", status_code=status.HTTP_200_OK)
async def update_answer(
    answer_uuid: UUID,
    request: AnswerUpdateRequest,
    answer_controller: AnswerController = Depends(Factory().get_answer_controller),
    user: User = Depends(AuthenticationRequired()),
) -> AnswerUpdateResponse:
    """Update an answer by its uuid."""
    return await answer_controller.update_answer(uuid=answer_uuid, data=request.model_dump(), request_user_id=user.id)


@router.delete("/{answer_uuid}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_answer(
    answer_uuid: UUID,
    answer_controller: AnswerController = Depends(Factory().get_answer_controller),
    user: User = Depends(AuthenticationRequired()),
) -> None:
    """Delete an answer by its uuid."""
    await answer_controller.delete_answer(uuid=answer_uuid, request_user_id=user.id)


@router.post("/{answer_uuid}/replies", status_code=status.HTTP_201_CREATED)
async def create_reply(
    answer_uuid: UUID,
    request: AnswerReplyCreateRequest,
    answer_controller: AnswerController = Depends(Factory().get_answer_controller),
    user: User = Depends(AuthenticationRequired()),
) -> AnswerCreateResponse:
    """Create a new reply to an answer."""
    data = request.model_dump()
    data["user_id"] = user.id
    return await answer_controller.create_reply(parent_uuid=answer_uuid, data=data)


@router.get("/{answer_uuid}/replies", status_code=status.HTTP_200_OK)
async def get_replies(
    answer_uuid: UUID,
    _=Depends(AuthenticationRequired()),
    answer_controller: AnswerController = Depends(Factory().get_answer_controller),
) -> Optional[list[AnswerResponse]]:
    """Get all replies to an answer."""
    return await answer_controller.retrieve_replies(parent_uuid=answer_uuid)
