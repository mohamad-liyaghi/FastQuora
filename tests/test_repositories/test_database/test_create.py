import pytest
from sqlalchemy.exc import IntegrityError, PendingRollbackError
from mocks import generate_fake_user_data


class TestDatabaseRepository:
    @pytest.fixture(autouse=True)
    def setup(self, test_session, database_repository):
        self.repository = database_repository
        self.data = generate_fake_user_data()

    @pytest.mark.asyncio
    async def test_create_with_valid_data_should_return_instance(self):
        instance = await self.repository.create(self.data)
        assert instance.id is not None
        assert instance.email == self.data.get("email")

    @pytest.mark.asyncio
    async def test_create_with_invalid_data_should_raise_exception(self):
        with pytest.raises(IntegrityError):
            await self.repository.create({})

    @pytest.mark.asyncio
    async def test_create_with_duplicate_data_should_raise_exception(self):
        with pytest.raises(PendingRollbackError):
            await self.repository.create(self.data)
