import pytest_asyncio
from app.controllers import AnswerController


@pytest_asyncio.fixture(scope="class")
async def answer_controller(test_session, test_redis_session):
    return AnswerController(session=test_session, redis_session=test_redis_session)
