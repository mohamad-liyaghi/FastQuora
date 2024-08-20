import pytest_asyncio
from app.models import User
from core.repositories import DatabaseRepository


@pytest_asyncio.fixture(scope="class")
async def database_repository(test_session):
    return DatabaseRepository(model=User, session=test_session)
