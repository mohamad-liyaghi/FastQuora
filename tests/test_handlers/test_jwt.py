import pytest
from uuid import uuid4
from core.handlers import JWTHandler


class TestJWTHandler:
    @pytest.mark.asyncio
    async def test_create_access_token(self):
        data = {"user_id": str(uuid4())}
        access_token = await JWTHandler.create_access_token(data)
        assert access_token is not None
        assert isinstance(access_token, str)
        assert access_token != ""
        assert access_token != "1234"
