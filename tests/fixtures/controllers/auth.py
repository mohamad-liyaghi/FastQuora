import pytest_asyncio
from app.controllers import AuthController


@pytest_asyncio.fixture(scope="class")
async def auth_controller(test_session, test_redis_session):
    return AuthController(session=test_session, redis_session=test_redis_session)
