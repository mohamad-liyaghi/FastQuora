import pytest_asyncio
from app.models import User
from core.repositories import ElasticRepository


@pytest_asyncio.fixture(scope="class")
async def elastic_repository():
    return ElasticRepository(User)
