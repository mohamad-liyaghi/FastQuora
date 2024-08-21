from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from fixtures.repositories import *  # noqa
from fixtures.models.user import *  # noqa
from fixtures.controllers import *  # noqa
from core.elastic import Elastic
from core.database import get_db, Base
from main import app
import pytest_asyncio
import pytest
import asyncio


@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()


@pytest_asyncio.fixture(scope="session", autouse=True)
async def clear_elastic():
    """
    Clear all indices in ElasticSearch
    """
    await Elastic.indices.delete(index="*", ignore=[400, 404])


@pytest_asyncio.fixture(scope="class")
async def test_session() -> AsyncSession:
    """
    Resets the database and returns a session
    """
    engine = create_async_engine("sqlite+aiosqlite:///:memory:")
    async_session = async_sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)

    async def override_get_db():
        async with async_session() as session:
            yield session

    app.dependency_overrides[get_db] = override_get_db  # noqa

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async for session in override_get_db():
        yield session
