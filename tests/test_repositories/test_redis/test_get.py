import pytest
from mocks import generate_fake_user_data


class TestRedisRepository:
    @pytest.fixture(autouse=True)
    def setup(self, redis_repository):
        self.repository = redis_repository
        self.data = generate_fake_user_data()

    @pytest.mark.asyncio
    async def test_get_non_existing_fails(self):
        user = await self.repository.get(1000)
        assert user is None

    @pytest.mark.asyncio
    async def test_get_existing(self):
        self.data["id"] = 1
        await self.repository.create(self.data)
        user = await self.repository.get(1)
        assert user == self.data
