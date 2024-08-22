import pytest
from mocks import generate_fake_user_data


class TestRedisRepository:
    @pytest.fixture(autouse=True)
    def setup(self, redis_repository):
        self.repository = redis_repository
        self.data = generate_fake_user_data()

    @pytest.mark.asyncio
    async def test_delete_non_existing_record_returns_none(self):
        data = await self.repository.delete(100)
        assert data is None

    @pytest.mark.asyncio
    async def test_delete_existing_record_deletes_record(self):
        self.data["id"] = 1
        await self.repository.create(self.data)
        await self.repository.delete(self.data["id"])
        data = await self.repository.get(self.data["id"])
        assert data is None
