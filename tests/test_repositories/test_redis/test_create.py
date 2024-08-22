import pytest
from mocks import generate_fake_user_data


class TestRedisRepository:
    @pytest.fixture(autouse=True)
    def setup(self, redis_repository):
        self.repository = redis_repository
        self.data = generate_fake_user_data()

    @pytest.mark.asyncio
    async def test_create_record(self):
        self.data["id"] = 1
        response = await self.repository.create(self.data)
        assert response == self.data

    @pytest.mark.asyncio
    async def test_create_without_id_raises_error(self):
        with pytest.raises(ValueError):
            await self.repository.create(self.data)

    @pytest.mark.asyncio
    async def test_create_duplicated_key_overrides_the_record(self):
        self.data["id"] = 1
        response = await self.repository.create(self.data)
        assert response == self.data
