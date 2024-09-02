import pytest
import pytest_asyncio
from fastapi import HTTPException
from app.enums.question import QuestionStatus


class TestAnswerCreateReply:
    @pytest_asyncio.fixture(autouse=True)
    async def setup(self, answer_controller, question):
        self.controller = answer_controller
        self.question = question

    @pytest.mark.asyncio
    async def test_create_for_closed_question_fails(self, question_controller, user, test_session):
        await self.controller.update(self.question, data={"status": QuestionStatus.CLOSED.value})
        with pytest.raises(HTTPException) as exc:
            await self.controller.create_reply(
                parent_uuid=self.question.uuid,
                data={"content": "Test content", "user_id": user.id},
            )

        assert exc.value.status_code == 404
        assert exc.value.detail == "Parent answer not found."

    @pytest.mark.asyncio
    async def test_create_for_deleted_question_fails(self, question_controller, user, test_session):
        await self.controller.update(self.question, data={"status": QuestionStatus.DELETED.value})
        with pytest.raises(HTTPException) as exc:
            await self.controller.create_reply(
                parent_uuid=self.question.uuid,
                data={"content": "Test content", "user_id": user.id},
            )

        assert exc.value.status_code == 404
        assert exc.value.detail == "Parent answer not found."
