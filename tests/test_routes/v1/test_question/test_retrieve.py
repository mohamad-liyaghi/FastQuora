import pytest
import pytest_asyncio
from fastapi import status
from httpx import AsyncClient
from uuid import uuid4


@pytest.mark.asyncio
class TestRetrieveQuestionRoute:
    @pytest_asyncio.fixture(autouse=True)
    async def setup_method(self, client: AsyncClient, question) -> None:
        self.url = f"v1/questions/{question.uuid}"

    @pytest.mark.asyncio
    async def test_retrieve_unauthorized_fails(self, client):
        response = await client.get(self.url)
        assert response.status_code == status.HTTP_403_FORBIDDEN

    @pytest.mark.asyncio
    async def test_retrieve_authorised_succeeds(self, authorized_client):
        response = await authorized_client.get(self.url)
        assert response.status_code == status.HTTP_200_OK

    @pytest.mark.asyncio
    async def test_retrieve_invalid_uuid_fails(self, authorized_client):
        response = await authorized_client.get(f"v1/questions/{uuid4()}")
        assert response.status_code == status.HTTP_404_NOT_FOUND
