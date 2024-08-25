import pytest
import pytest_asyncio
from fastapi import status
from uuid import uuid4
from httpx import AsyncClient


@pytest.mark.asyncio
class TestRetrieveProfileRoute:
    @pytest_asyncio.fixture(autouse=True)
    async def setup_method(self, user) -> None:
        self.url = f"v1/profile/{user.uuid}"

    @pytest.mark.asyncio
    async def test_retrieve_unauthorized_fails(self, client) -> None:
        response = await client.get(self.url)
        assert response.status_code == status.HTTP_403_FORBIDDEN

    @pytest.mark.asyncio
    async def test_retrieve_profile(self, authorized_client) -> None:
        response = await authorized_client.get(self.url)
        assert response.status_code == status.HTTP_200_OK

    @pytest.mark.asyncio
    async def test_retrieve_with_invalid_uuid(self, authorized_client) -> None:
        response = await authorized_client.get(f"v1/profile/{uuid4()}")
        assert response.status_code == status.HTTP_404_NOT_FOUND
