import pytest_asyncio
import pytest
from fastapi import HTTPException
from uuid import uuid4


class TestProfileController:
    @pytest_asyncio.fixture(autouse=True)
    async def setup(self, profile_controller, user):
        self.controller = profile_controller
        self.user = user

    @pytest.mark.asyncio
    async def test_get_by_uuid(self):
        user = await self.controller.get_by_uuid(self.user.uuid)
        assert user.uuid == self.user.uuid

    @pytest.mark.asyncio
    async def test_get_invalid_uuid_fails(self):
        with pytest.raises(HTTPException):
            await self.controller.get_by_uuid(uuid4())
