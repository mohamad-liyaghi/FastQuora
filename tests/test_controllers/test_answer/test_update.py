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

    @pytest.mark.asyncio
    async def test_update_by_owner_succeeds(self, test_session):
        new_content = "New content"
        await self.controller.update_answer(
            uuid=self.answer.uuid,
            data={"content": new_content},
            request_user_id=self.answer.user_id,
        )
        answer = await self.controller.retrieve(uuid=self.answer.uuid)
        assert answer.content == new_content
