import pytest
import pytest_asyncio
from fastapi import status


@pytest.mark.asyncio
class TestListAnswerRepliesRoute:
    @pytest_asyncio.fixture(autouse=True)
    async def setup_method(self, answer) -> None:
        self.url = f"v1/answers/{answer.uuid}/replies"

    @pytest.mark.asyncio
    async def test_list_unauthorized_fails(self, client):
        response = await client.get(self.url)
        assert response.status_code == status.HTTP_403_FORBIDDEN

    @pytest.mark.asyncio
    async def test_list_with_valid_data_succeeds(self, authorized_client, answer):
        response = await authorized_client.get(self.url)
        assert response.status_code == status.HTTP_200_OK
