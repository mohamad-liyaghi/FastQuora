import pytest_asyncio
from app.models import Vote
from app.enums.vote import VoteType


@pytest_asyncio.fixture(scope="class")
async def vote(user, answer, vote_controller) -> Vote:
    vote = await vote_controller.create(user_id=user.id, answer_id=answer.id, vote_type=VoteType.UP)
    return vote


@pytest_asyncio.fixture(scope="class")
async def another_vote(another_answer, another_user, vote_controller) -> Vote:
    return await vote_controller.create(user_id=another_user.id, answer_id=another_answer.id, vote_type=VoteType.DOWN)
