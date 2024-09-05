import pytest
import pytest_asyncio
from app.enums.vote import VoteType


class TestVoteCreate:
    @pytest_asyncio.fixture(autouse=True)
    async def setup(self, vote_controller, question, user):
        self.controller = vote_controller
        self.question = question
        self.user = user

    @pytest.mark.asyncio
    async def test_create_vote(self):
        vote = await self.controller.create_vote(
            question_id=self.question.id, user_id=self.user.id, vote=VoteType.UP.value
        )
        assert vote["question_id"] == self.question.id
        assert vote["user_id"] == self.user.id
        assert vote["vote"] == VoteType.UP.value

    @pytest.mark.asyncio
    async def test_create_vote_twice_updates_the_older_vote(self):
        vote = await self.controller.create_vote(
            question_id=self.question.id, user_id=self.user.id, vote=VoteType.DOWN.value
        )
        assert vote["question_id"] == self.question.id
        assert vote["user_id"] == self.user.id
        assert vote["vote"] == VoteType.DOWN.value
