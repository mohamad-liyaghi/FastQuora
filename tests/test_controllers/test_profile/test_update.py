import pytest_asyncio
import pytest
from fastapi import HTTPException
from uuid import uuid4


class TestProfileController:
    @pytest_asyncio.fixture(autouse=True)
    async def setup(self, profile_controller, user):
        self.controller = profile_controller
        self.user = user
        self.data = {
            "email": "another@email.com",
            "nickname": "another_nickname",
            "biography": "Another biography",
        }

    @pytest.mark.asyncio
    async def test_update_profile(self):
        profile = await self.controller.update_user(self.user.uuid, self.user, self.data)
        assert profile.email == self.data["email"]
        assert profile.nickname == self.data["nickname"]
        assert profile.biography == self.data["biography"]

    @pytest.mark.asyncio
    async def test_update_profile_with_invalid_data(self):
        with pytest.raises(HTTPException):
            await self.controller.update_user(self.user.uuid, self.user, {})

    @pytest.mark.asyncio
    async def test_update_existing_email_fails(self, another_user):
        with pytest.raises(HTTPException):
            await self.controller.update_user(self.user.uuid, self.user, {"email": another_user.email})

    @pytest.mark.asyncio
    async def test_update_existing_nickname_fails(self, another_user):
        with pytest.raises(HTTPException):
            await self.controller.update_user(self.user.uuid, self.user, {"nickname": another_user.nickname})
