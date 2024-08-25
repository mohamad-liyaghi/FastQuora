import pytest_asyncio
from app.controllers import ProfileController


@pytest_asyncio.fixture(scope="class")
async def profile_controller(test_session, test_redis_session):
    return ProfileController(session=test_session, redis_session=test_redis_session)
