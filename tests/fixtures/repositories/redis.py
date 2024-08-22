import pytest_asyncio
from app.models import User
from core.repositories import RedisRepository


@pytest_asyncio.fixture(scope="class")
async def redis_repository(test_redis_session):
    return RedisRepository(User, test_redis_session)
