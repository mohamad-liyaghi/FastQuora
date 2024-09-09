from fastapi.routing import APIRouter
from fastapi import Depends, status
from uuid import UUID
from core.factory import Factory
from app.controllers import VoteController, AnswerController
from app.models import User
from core.dependencies import AuthenticationRequired
from app.schemas.requests.vote import VoteCreateRequest
from app.schemas.responses.vote import VoteCreateResponse


router = APIRouter(tags=["Vote"])


@router.post("/{answer_uuid}", status_code=status.HTTP_201_CREATED)
async def create_vote(
    answer_uuid: UUID,
    vote: VoteCreateRequest,
    vote_controller: VoteController = Depends(Factory().get_vote_controller),
    answer_controller: AnswerController = Depends(Factory().get_answer_controller),
    user: User = Depends(AuthenticationRequired()),
) -> VoteCreateResponse:
    """Create a new vote."""
    return await vote_controller.create_vote(
        answer_uuid=answer_uuid,
        user_id=user.id,
        vote=vote.vote.value,
        answer_controller=answer_controller,
    )
