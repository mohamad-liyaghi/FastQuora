import pytest
import pytest_asyncio
from fastapi import status
from httpx import AsyncClient
from mocks import generate_fake_user_data


@pytest.mark.asyncio
class TestLoginRoute:
    @pytest_asyncio.fixture(autouse=True)
    async def setup_method(self, client: AsyncClient, auth_controller) -> None:
        self.user_data = generate_fake_user_data()
        self.user = await auth_controller.register(data=self.user_data)
        self.data = {
            "email": self.user_data.get("email"),
            "password": self.user_data.get("password"),
        }
        self.client = client
        self.url = "v1/auth/login"

    @pytest.mark.asyncio
    async def test_login_valid_credentials(self) -> None:
        response = await self.client.post(self.url, json=self.data)
        assert response.status_code == status.HTTP_200_OK

    @pytest.mark.asyncio
    async def test_login_with_invalid_password_fails(self) -> None:
        self.data["password"] = "Invalid Password"
        response = await self.client.post(self.url, json=self.data)
        assert response.status_code == status.HTTP_403_FORBIDDEN

    @pytest.mark.asyncio
    async def test_login_with_invalid_email_fails(self) -> None:
        self.data["email"] = "non@existance.com"
        response = await self.client.post(self.url, json=self.data)
        assert response.status_code == status.HTTP_404_NOT_FOUND

    @pytest.mark.asyncio
    async def test_login_with_invalid_data_fails(self) -> None:
        response = await self.client.post(self.url)
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
