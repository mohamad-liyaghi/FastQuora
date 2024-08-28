import pytest
import pytest_asyncio
from fastapi import HTTPException
from uuid import uuid4
from app.enums.question import QuestionStatus


class TestQuestionDelete:
    @pytest_asyncio.fixture(autouse=True)
    async def setup(self, question_controller, question):
        self.controller = question_controller
        self.question = question

    @pytest.mark.asyncio
    async def test_delete_question_by_another_user_fails(self, another_user):
        with pytest.raises(HTTPException) as exc:
            await self.controller.delete_question(uuid=self.question.uuid, user_id=another_user.id)
        assert exc.value.status_code == 403
        assert exc.value.detail == "Forbidden"

    @pytest.mark.asyncio
    async def test_delete_non_existing_question_fails(self):
        with pytest.raises(HTTPException) as exc:
            await self.controller.delete_question(uuid=uuid4(), user_id=self.question.user_id)
        assert exc.value.status_code == 404
        assert exc.value.detail == "Question not found"

    @pytest.mark.asyncio
    async def test_delete_question_by_owner_succeeds(self):
        await self.controller.delete_question(uuid=self.question.uuid, user_id=self.question.user_id)
        question = await self.controller.retrieve(uuid=self.question.uuid)
        assert question.status == QuestionStatus.DELETED.value
