import pytest
import pytest_asyncio
from fastapi import HTTPException
from uuid import uuid4
from app.enums.question import QuestionStatus


class TestQuestionRetrieve:
    @pytest_asyncio.fixture(autouse=True)
    async def setup(self, question_controller, question):
        self.controller = question_controller
        self.question = question

    @pytest.mark.asyncio
    async def test_retrieve_by_uuid(self):
        retrieved_question = await self.controller.retrieve_by_uuid(uuid=self.question.uuid)
        assert retrieved_question == self.question

    @pytest.mark.asyncio
    async def test_retrieve_by_uuid_not_found(self):
        with pytest.raises(HTTPException) as exc:
            await self.controller.retrieve_by_uuid(uuid=uuid4())
        assert exc.value.status_code == 404

    @pytest.mark.asyncio
    async def test_retrieve_deleted_question_fails(self):
        await self.controller.update(self.question, data={"status": QuestionStatus.DELETED.value})
        with pytest.raises(HTTPException) as exc:
            await self.controller.retrieve_by_uuid(uuid=self.question.uuid)
        assert exc.value.status_code == 404
