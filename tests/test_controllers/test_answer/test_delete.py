import pytest
import pytest_asyncio
from fastapi import HTTPException


class TestAnswerDelete:
    @pytest_asyncio.fixture(autouse=True)
    async def setup(self, answer_controller, answer):
        self.controller = answer_controller
        self.answer = answer

    @pytest.mark.asyncio
    async def test_delete_by_non_owner_fails(self, another_user, test_session):
        with pytest.raises(HTTPException) as exc:
            await self.controller.delete_answer(uuid=self.answer.uuid, request_user_id=another_user.id)
        assert exc.value.status_code == 403
        assert exc.value.detail == "You are not allowed to delete this answer."

    @pytest.mark.asyncio
    async def test_delete_by_owner_succeeds(self, test_session):
        await self.controller.delete_answer(uuid=self.answer.uuid, request_user_id=self.answer.user_id)
        answer = await self.controller.retrieve(uuid=self.answer.uuid)
        assert answer.is_deleted is True
