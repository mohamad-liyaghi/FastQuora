import pytest
import pytest_asyncio
from fastapi import status


@pytest.mark.asyncio
class TestUpdateAnswerRoute:
    @pytest_asyncio.fixture(autouse=True)
    async def setup_method(self, answer) -> None:
        self.url = f"v1/answers/{answer.uuid}"
        self.data = {"content": "This is the updated answer."}

    @pytest.mark.asyncio
    async def test_update_unauthorized_fails(self, client):
        response = await client.put(self.url, json={})
        assert response.status_code == status.HTTP_403_FORBIDDEN

    @pytest.mark.asyncio
    async def test_update_with_invalid_data_fails(self, authorized_client):
        response = await authorized_client.put(self.url, json={})
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    @pytest.mark.asyncio
    async def test_update_with_valid_data_succeeds(self, authorized_client, question):
        response = await authorized_client.put(self.url, json=self.data)
        assert response.status_code == status.HTTP_200_OK

    @pytest.mark.asyncio
    async def test_update_by_another_user_fails(self, another_authorized_client):
        response = await another_authorized_client.put(self.url, json=self.data)
        assert response.status_code == status.HTTP_404_NOT_FOUND
