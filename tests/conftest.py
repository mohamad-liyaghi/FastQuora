import pytest
import pytest_asyncio  # noqa
import asyncio
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from core.database import get_db, Base
from main import app

engine = create_async_engine("sqlite+aiosqlite:///:memory:")


async def override_get_db():
    async_session = async_sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)
    async with async_session() as session:
        yield session


app.dependency_overrides[get_db] = override_get_db  # noqa


@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()


@pytest_asyncio.fixture(scope="session")
async def test_session() -> AsyncSession:
    """
    Resets the database and returns a session
    """

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async for session in override_get_db():
        yield session
