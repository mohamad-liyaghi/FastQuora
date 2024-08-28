import pytest
import pytest_asyncio


class TestBaseController:
    @pytest_asyncio.fixture(autouse=True)
    async def setup(self, test_session, user, base_controller):
        self.controller = base_controller
        self.user = user

    @pytest.mark.asyncio
    async def test_retrieve_by_id(self):
        user = await self.controller.retrieve(id=self.user.id)
        assert user == self.user

    @pytest.mark.asyncio
    async def test_retrieve_by_email(self):
        user = await self.controller.retrieve(email=self.user.email)
        assert user == self.user

    @pytest.mark.asyncio
    async def test_retrieve_non_existing_user(self):
        user = await self.controller.retrieve(id=100)
        assert user is None
