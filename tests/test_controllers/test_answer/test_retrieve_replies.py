import pytest
import pytest_asyncio


class TestAnswerCreateReply:
    @pytest_asyncio.fixture(autouse=True)
    async def setup(self, answer_controller, question, answer):
        self.controller = answer_controller
        self.question = question
        self.answer = answer

    @pytest.mark.asyncio
    async def test_get_empty_replies(self):
        replies = await self.controller.retrieve_replies(parent_uuid=self.answer.uuid)
        assert not replies

    @pytest.mark.asyncio
    async def test_get_replies(self, answer_with_parent):
        replies = await self.controller.retrieve_replies(parent_uuid=self.answer.uuid)
        assert replies
