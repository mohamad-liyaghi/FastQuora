import pytest
import pytest_asyncio
from fastapi import status
from uuid import uuid4
from app.enums.vote import VoteType


@pytest.mark.asyncio
class TestCreateViteRoute:
    @pytest_asyncio.fixture(autouse=True)
    async def setup_method(self, answer) -> None:
        self.url = f"v1/votes/{answer.uuid}"

    @pytest.mark.asyncio
    async def test_create_unauthorized_fails(self, client):
        response = await client.post(self.url, json={})
        assert response.status_code == status.HTTP_403_FORBIDDEN

    @pytest.mark.asyncio
    async def test_create_with_invalid_data_fails(self, authorized_client):
        response = await authorized_client.post(self.url, json={})
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    @pytest.mark.asyncio
    async def test_create_for_invalid_answer_fails(self, authorized_client):
        response = await authorized_client.post(f"v1/votes/{str(uuid4())}", json={"vote": VoteType.DOWN.value})
        assert response.status_code == status.HTTP_404_NOT_FOUND

    @pytest.mark.asyncio
    async def test_create_with_valid_data_succeeds(self, authorized_client, answer):
        response = await authorized_client.post(self.url, json={"vote": VoteType.UP.value})
        assert response.status_code == status.HTTP_201_CREATED
