import pytest
import pytest_asyncio


class TestBaseController:
    @pytest_asyncio.fixture(autouse=True)
    async def setup(self, test_session, user, base_controller):
        self.controller = base_controller
        self.user = user

    @pytest.mark.asyncio
    async def test_delete_user(self):
        await self.controller.delete(self.user)
        user = await self.controller.retrieve(id=self.user.id)
        assert user is None
