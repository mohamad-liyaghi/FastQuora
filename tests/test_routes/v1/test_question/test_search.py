import pytest
import pytest_asyncio
from fastapi import status
from httpx import AsyncClient
from uuid import uuid4


@pytest.mark.asyncio
class TestSearchQuestionRoute:
    @pytest_asyncio.fixture(autouse=True)
    async def setup_method(self, client: AsyncClient, question) -> None:
        self.url = f"v1/questions/?q={question.title}"

    @pytest.mark.asyncio
    async def test_search_unauthorized_fails(self, client: AsyncClient) -> None:
        response = await client.get(self.url)
        assert response.status_code == status.HTTP_403_FORBIDDEN

    @pytest.mark.asyncio
    async def test_search_question_succeeds(self, authorized_client) -> None:
        response = await authorized_client.get(self.url)
        assert response.status_code == status.HTTP_200_OK

    @pytest.mark.asyncio
    async def test_search_with_invalid_query_fails(self, authorized_client) -> None:
        response = await authorized_client.get("v1/questions/?q=invalid")
        assert response.status_code == status.HTTP_200_OK
        assert not response.json()
