import pytest
from mocks import generate_fake_user_data


class TestAuthController:
    @pytest.fixture(autouse=True)
    def setup(self, test_session, auth_controller):
        self.controller = auth_controller
        self.data = generate_fake_user_data()

    @pytest.mark.asyncio
    async def test_register_creates_user(self):
        user = await self.controller.register(data=self.data)
        assert user.id is not None

    @pytest.mark.asyncio
    async def test_register_hashes_password(self):
        user = await self.controller.register(data=self.data)
        assert user.password != self.data["password"]
