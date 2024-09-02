import pytest
import pytest_asyncio
from fastapi import status


@pytest.mark.asyncio
class TestCreateAnswerRoute:
    @pytest_asyncio.fixture(autouse=True)
    async def setup_method(self, answer) -> None:
        self.url = f"v1/answers/{answer.uuid}/replies"

    @pytest.mark.asyncio
    async def test_create_unauthorized_fails(self, client):
        response = await client.post(self.url, json={})
        assert response.status_code == status.HTTP_403_FORBIDDEN

    @pytest.mark.asyncio
    async def test_create_with_invalid_data_fails(self, authorized_client):
        response = await authorized_client.post(self.url, json={})
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    @pytest.mark.asyncio
    async def test_create_with_valid_data_succeeds(self, authorized_client, question):
        response = await authorized_client.post(
            self.url,
            json={"content": "This is a test answer."},
        )
        assert response.status_code == status.HTTP_201_CREATED
