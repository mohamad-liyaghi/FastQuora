import pytest
import pytest_asyncio
from app.models import User
from core.repositories import DatabaseRepository


class TestDatabaseRepository:
    @pytest_asyncio.fixture(autouse=True)
    async def setup(self, test_session, user):
        self.repository = DatabaseRepository(model=User, session=test_session)
        self.user = user

    @pytest.mark.asyncio
    async def test_retrieve_by_id(self):
        user = await self.repository.retrieve(id=self.user.id)
        assert user == self.user

    @pytest.mark.asyncio
    async def test_retrieve_by_email(self):
        user = await self.repository.retrieve(email=self.user.email)
        assert user == self.user

    @pytest.mark.asyncio
    async def test_retrieve_non_existing_user(self):
        user = await self.repository.retrieve(id=100)
        assert user is None
