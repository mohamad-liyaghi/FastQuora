import pytest
import pytest_asyncio
from fastapi import status
from httpx import AsyncClient
from mocks import generate_fake_user_data


@pytest.mark.asyncio
class TestRegisterRoute:
    @pytest_asyncio.fixture(autouse=True)
    async def setup_method(self, client: AsyncClient) -> None:
        credential = generate_fake_user_data()
        self.data = {
            "email": credential["email"],
            "nickname": credential["nickname"],
            "biography": credential["biography"],
            "password": credential["password"],
        }
        self.client = client
        self.url = "v1/auth/register"

    @pytest.mark.asyncio
    async def test_register_user_with_valid_data(self) -> None:
        response = await self.client.post(self.url, json=self.data)
        assert response.status_code == status.HTTP_201_CREATED

    @pytest.mark.asyncio
    async def test_register_user_invalid_data_fails(self) -> None:
        response = await self.client.post(self.url)
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    @pytest.mark.asyncio
    async def test_register_with_duplicate_email_fails(self, user):
        self.data["email"] = user.email
        response = await self.client.post(self.url, json=self.data)
        assert response.status_code == status.HTTP_409_CONFLICT

    @pytest.mark.asyncio
    async def test_register_with_duplicated_nickname_fails(self, user):
        self.data["nickname"] = user.nickname
        response = await self.client.post(self.url, json=self.data)
        assert response.status_code == status.HTTP_409_CONFLICT
