import pytest
import pytest_asyncio
from fastapi import HTTPException
from uuid import uuid4


class TestQuestionUpdate:
    @pytest_asyncio.fixture(autouse=True)
    async def setup(self, question_controller, question):
        self.controller = question_controller
        self.question = question

    @pytest.mark.asyncio
    async def test_update_question_not_found(self):
        with pytest.raises(HTTPException) as exc:
            await self.controller.update_question(uuid=uuid4(), data={}, user_id=self.question.user_id)
        assert exc.value.status_code == 404
        assert exc.value.detail == "Question not found"

    @pytest.mark.asyncio
    async def test_update_question_by_non_owner_fails(self, another_question):
        with pytest.raises(HTTPException) as exc:
            await self.controller.update_question(uuid=another_question.uuid, data={}, user_id=self.question.user_id)
        assert exc.value.status_code == 403
        assert exc.value.detail == "Forbidden"

    @pytest.mark.asyncio
    async def test_update_question_success(self):
        new_title = "Updated Title"
        updated_question = await self.controller.update_question(
            uuid=self.question.uuid,
            data={"title": new_title},
            user_id=self.question.user_id,
        )
        assert updated_question.title == new_title
