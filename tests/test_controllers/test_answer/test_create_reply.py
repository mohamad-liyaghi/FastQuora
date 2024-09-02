import pytest
import pytest_asyncio
from fastapi import HTTPException
from uuid import uuid4
from app.enums.question import QuestionStatus


class TestAnswerCreateReply:
    @pytest_asyncio.fixture(autouse=True)
    async def setup(self, answer_controller, answer, question):
        self.controller = answer_controller
        self.question = question
        self.answer = answer

    @pytest.mark.asyncio
    async def test_create_for_closed_question_fails(self, question_controller, user, test_session):
        await self.controller.update(self.question, data={"status": QuestionStatus.CLOSED.value})
        with pytest.raises(HTTPException) as exc:
            await self.controller.create_reply(
                parent_uuid=self.answer.uuid,
                data={"content": "Test content", "user_id": user.id},
            )

        assert exc.value.status_code == 400
        assert exc.value.detail == "Parent question is closed or deleted."

    @pytest.mark.asyncio
    async def test_create_for_deleted_question_fails(self, question_controller, user, test_session):
        await self.controller.update(self.question, data={"status": QuestionStatus.DELETED.value})
        with pytest.raises(HTTPException) as exc:
            await self.controller.create_reply(
                parent_uuid=self.answer.uuid,
                data={"content": "Test content", "user_id": user.id},
            )

        assert exc.value.status_code == 400
        assert exc.value.detail == "Parent question is closed or deleted."

    @pytest.mark.asyncio
    async def test_create_for_invalid_parent_fails(self, user):
        with pytest.raises(HTTPException) as exc:
            await self.controller.create_reply(
                parent_uuid=uuid4(),
                data={"content": "Test content", "user_id": user.id},
            )

        assert exc.value.status_code == 404
        assert exc.value.detail == "Parent answer not found."
