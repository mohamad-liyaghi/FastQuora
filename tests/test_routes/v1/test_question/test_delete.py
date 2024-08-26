import pytest
import pytest_asyncio
from fastapi import status


@pytest.mark.asyncio
class TestCreateQuestionRoute:
    @pytest_asyncio.fixture(autouse=True)
    async def setup_method(self, question) -> None:
        self.url = f"v1/questions/{question.uuid}"

    @pytest.mark.asyncio
    async def test_delete_unauthorized_fails(self, client):
        response = await client.delete(self.url)
        assert response.status_code == status.HTTP_403_FORBIDDEN

    @pytest.mark.asyncio
    async def test_delete_by_owner_succeeds(self, authorized_client):
        response = await authorized_client.delete(self.url)
        assert response.status_code == status.HTTP_204_NO_CONTENT

    @pytest.mark.asyncio
    async def test_delete_by_another_user_fails(self, another_question, authorized_client):
        response = await authorized_client.delete(f"v1/questions/{another_question.uuid}")
        assert response.status_code == status.HTTP_403_FORBIDDEN
