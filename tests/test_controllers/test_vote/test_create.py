import pytest
import pytest_asyncio
from uuid import uuid4
from fastapi import HTTPException
from app.enums.vote import VoteType


class TestVoteCreate:
    @pytest_asyncio.fixture(autouse=True)
    async def setup(self, vote_controller, answer, user, answer_controller):
        self.controller = vote_controller
        self.answer_controller = answer_controller
        self.answer = answer
        self.user = user

    @pytest.mark.asyncio
    async def test_create_vote(self):
        vote = await self.controller.create_vote(
            answer_uuid=self.answer.uuid,
            user_id=self.user.id,
            vote=VoteType.UP.value,
            answer_controller=self.answer_controller,
        )
        assert vote["answer_id"] == self.answer.id
        assert vote["user_id"] == self.user.id
        assert vote["vote"] == VoteType.UP.value

    @pytest.mark.asyncio
    async def test_create_vote_twice_updates_the_older_vote(self):
        vote = await self.controller.create_vote(
            answer_uuid=self.answer.uuid,
            user_id=self.user.id,
            vote=VoteType.DOWN.value,
            answer_controller=self.answer_controller,
        )
        assert vote["answer_id"] == self.answer.id
        assert vote["user_id"] == self.user.id
        assert vote["vote"] == VoteType.DOWN.value

    @pytest.mark.asyncio
    async def test_create_for_invalid_answer_fails(self):
        with pytest.raises(HTTPException):
            await self.controller.create_vote(
                answer_uuid=uuid4(),
                user_id=self.user.id,
                vote=VoteType.DOWN.value,
                answer_controller=self.answer_controller,
            )
