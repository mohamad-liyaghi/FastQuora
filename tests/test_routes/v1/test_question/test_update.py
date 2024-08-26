import pytest
import pytest_asyncio
from fastapi import status
from httpx import AsyncClient
from uuid import uuid4


@pytest.mark.asyncio
class TestUpdateQuestionRoute:
    @pytest_asyncio.fixture(autouse=True)
    async def setup_method(self, client: AsyncClient, question) -> None:
        self.url = f"v1/questions/{question.uuid}"
        self.data = {
            "title": "Updated Title",
            "content": "Updated Content",
        }

    @pytest.mark.asyncio
    async def test_update_unauthorized_fails(self, client: AsyncClient, question) -> None:
        response = await client.put(self.url, json=self.data)
        assert response.status_code == status.HTTP_403_FORBIDDEN

    @pytest.mark.asyncio
    async def test_update_by_another_user_fails(self, another_authorized_client):
        response = await another_authorized_client.put(self.url, json=self.data)
        assert response.status_code == status.HTTP_403_FORBIDDEN

    @pytest.mark.asyncio
    async def test_update_question_succeeds(self, authorized_client, question) -> None:
        response = await authorized_client.put(self.url, json=self.data)
        assert response.status_code == status.HTTP_200_OK

    @pytest.mark.asyncio
    async def test_update_with_invalid_uuid_fails(self, authorized_client) -> None:
        url = f"v1/questions/{uuid4()}"
        response = await authorized_client.put(url, json=self.data)
        assert response.status_code == status.HTTP_404_NOT_FOUND
