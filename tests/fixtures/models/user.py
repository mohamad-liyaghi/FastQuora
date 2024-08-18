import pytest_asyncio
from app.models import User
from mocks import generate_fake_user_data


@pytest_asyncio.fixture(scope="session")
async def user(database_repository) -> User:
    data = generate_fake_user_data()
    return await database_repository.create(data)


@pytest_asyncio.fixture(scope="session")
async def another_user(database_repository) -> User:
    data = generate_fake_user_data()
    return await database_repository.create(data)
