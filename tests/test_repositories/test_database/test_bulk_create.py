import pytest
from mocks import generate_fake_user_data


class TestDatabaseRepository:
    @pytest.fixture(autouse=True)
    def setup(self, test_session, database_repository):
        self.repository = database_repository
        self.data = generate_fake_user_data()
        self.another_data = generate_fake_user_data()

    @pytest.mark.asyncio
    async def test_create_with_valid_data_should_return_instance(self):
        instances = await self.repository.bulk_create([self.data, self.another_data])
        assert len(instances) == 2

    @pytest.mark.asyncio
    async def test_create_with_invalid_data_should_raise_integrity_error(self):
        with pytest.raises(ValueError):
            await self.repository.bulk_create([])
