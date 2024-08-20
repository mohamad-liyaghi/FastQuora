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
    async def test_delete_user(self):
        await self.repository.delete(self.user)
        user = await self.repository.retrieve(id=self.user.id)
        assert user is None
