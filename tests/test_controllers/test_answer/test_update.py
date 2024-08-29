import pytest
import pytest_asyncio
from fastapi import HTTPException


class TestAnswerUpdate:
    @pytest_asyncio.fixture(autouse=True)
    async def setup(self, answer_controller, answer):
        self.controller = answer_controller
        self.answer = answer

    @pytest.mark.asyncio
    async def test_update_by_non_owner_fails(self, user, test_session):
        with pytest.raises(HTTPException) as exc:
            await self.controller.update_answer(
                uuid=self.answer.uuid,
                data={"content": "Test content"},
                request_user_id=user.id + 1,
            )

        assert exc.value.status_code == 404
        assert exc.value.detail == "Answer not found."
