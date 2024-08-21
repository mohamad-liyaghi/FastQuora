import pytest_asyncio
from app.models import User
from core.repositories import ElasticRepository


@pytest_asyncio.fixture(scope="class")
async def elastic_repository():
    return ElasticRepository(User)


@pytest_asyncio.fixture(scope="class")
async def elastic_record(elastic_repository, user):
    return await elastic_repository.create(
        {
            "id": user.id,
            "email": user.email,
            "nickname": user.nickname,
        }
    )
