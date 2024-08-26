import pytest_asyncio
from app.controllers import QuestionController


@pytest_asyncio.fixture(scope="class")
async def question_controller(test_session, test_redis_session):
    return QuestionController(session=test_session, redis_session=test_redis_session)
