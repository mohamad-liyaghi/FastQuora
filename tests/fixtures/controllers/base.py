import pytest_asyncio
from app.models import User
from core.controllers import BaseController


@pytest_asyncio.fixture(scope="class")
async def base_controller(test_session, test_redis_session):
    return BaseController(model=User, session=test_session, redis_session=test_redis_session)
