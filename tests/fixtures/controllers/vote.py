import pytest_asyncio
from app.controllers import VoteController


@pytest_asyncio.fixture(scope="class")
async def vote_controller(test_session, test_redis_session):
    return VoteController(session=test_session, redis_session=test_redis_session)
