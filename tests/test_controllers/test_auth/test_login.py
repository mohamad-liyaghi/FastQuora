import pytest_asyncio
import pytest
from fastapi import HTTPException
from mocks import generate_fake_user_data


class TestAuthController:
    @pytest_asyncio.fixture(autouse=True)
    async def setup(self, test_session, auth_controller):
        self.controller = auth_controller
        self.data = generate_fake_user_data()
        self.user = await self.controller.register(data=self.data)

    @pytest.mark.asyncio
    async def test_create_access_token_with_valid_data(self):
        token = await self.controller.login(email=self.data.get("email"), password=self.data.get("password"))
        assert token

    @pytest.mark.asyncio
    async def test_create_with_invalid_password_fails(self):
        with pytest.raises(HTTPException):
            await self.controller.login(email=self.data.get("email"), password="invalid_password")

    @pytest.mark.asyncio
    async def test_create_for_invalid_email_fails(self):
        with pytest.raises(HTTPException):
            await self.controller.login(email="invalid_email", password=self.data.get("password"))
