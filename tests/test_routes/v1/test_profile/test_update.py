import pytest
import pytest_asyncio
from fastapi import status
from uuid import uuid4


@pytest.mark.asyncio
class TestUpdateProfileRoute:
    @pytest_asyncio.fixture(autouse=True)
    async def setup_method(self, user) -> None:
        self.url = f"v1/profiles/{user.uuid}"
        self.data = {
            "biography": "New biography",
            "email": "updated@email.com",
            "nickname": "updated_nickname",
        }

    @pytest.mark.asyncio
    async def test_update_unauthorized_fails(self, client):
        response = await client.put(self.url, json=self.data)
        assert response.status_code == status.HTTP_403_FORBIDDEN

    @pytest.mark.asyncio
    async def test_update_with_invalid_data_fails(self, authorized_client):
        response = await authorized_client.put(self.url, json={})
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    @pytest.mark.asyncio
    async def test_update_with_valid_data_succeeds(self, authorized_client):
        response = await authorized_client.put(self.url, json=self.data)
        assert response.status_code == status.HTTP_200_OK
        assert response.json()["biography"] == self.data["biography"]

    @pytest.mark.asyncio
    async def test_update_by_another_user_fails(self, another_authorized_client):
        response = await another_authorized_client.put(self.url, json=self.data)
        assert response.status_code == status.HTTP_403_FORBIDDEN

    @pytest.mark.asyncio
    async def test_update_with_duplicated_email_fails(self, user, another_user, another_authorized_client):
        response = await another_authorized_client.put(f"v1/profiles/{another_user.uuid}", json=self.data)
        assert response.status_code == status.HTTP_409_CONFLICT

    @pytest.mark.asyncio
    async def test_update_with_duplicated_nickname_fails(self, another_user, another_authorized_client, user):
        self.data["email"] = another_user.email
        response = await another_authorized_client.put(f"v1/profiles/{another_user.uuid}", json=self.data)
        assert response.status_code == status.HTTP_409_CONFLICT

    @pytest.mark.asyncio
    async def test_update_for_invalid_uuid_fails(self, authorized_client):
        response = await authorized_client.put(f"v1/profiles/{uuid4()}", json=self.data)
        assert response.status_code == status.HTTP_404_NOT_FOUND
