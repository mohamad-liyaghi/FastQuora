import pytest
import pytest_asyncio
from app.enums.vote import VoteType


class TestVoteCreate:
    @pytest_asyncio.fixture(autouse=True)
    async def setup(self, vote_controller, answer, user):
        self.controller = vote_controller
        self.answer = answer
        self.user = user

    @pytest.mark.asyncio
    async def test_create_vote(self):
        vote = await self.controller.create_vote(answer_id=self.answer.id, user_id=self.user.id, vote=VoteType.UP.value)
        assert vote["answer_id"] == self.answer.id
        assert vote["user_id"] == self.user.id
        assert vote["vote"] == VoteType.UP.value

    @pytest.mark.asyncio
    async def test_create_vote_twice_updates_the_older_vote(self):
        vote = await self.controller.create_vote(
            answer_id=self.answer.id, user_id=self.user.id, vote=VoteType.DOWN.value
        )
        assert vote["answer_id"] == self.answer.id
        assert vote["user_id"] == self.user.id
        assert vote["vote"] == VoteType.DOWN.value
