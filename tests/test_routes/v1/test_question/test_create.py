import pytest
import pytest_asyncio
from fastapi import status
from httpx import AsyncClient


@pytest.mark.asyncio
class TestRegisterRoute:
    @pytest_asyncio.fixture(autouse=True)
    async def setup_method(self, client: AsyncClient) -> None:
        self.data = {
            "title": "Test Title",
            "content": "Test Content",
        }
        self.client = client
        self.url = "v1/questions/"

    @pytest.mark.asyncio
    async def test_create_unauthorized_fails(self, client):
        response = await client.post(self.url, json=self.data)
        assert response.status_code == status.HTTP_403_FORBIDDEN

    @pytest.mark.asyncio
    async def test_create_with_invalid_data_fails(self, authorized_client):
        response = await authorized_client.post(self.url, json={})
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    @pytest.mark.asyncio
    async def test_create_with_valid_data_succeeds(self, authorized_client):
        response = await authorized_client.post(self.url, json=self.data)
        assert response.status_code == status.HTTP_201_CREATED
        assert response.json()["title"] == self.data["title"]
        assert response.json()["content"] == self.data["content"]
