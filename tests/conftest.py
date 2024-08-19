import pytest_asyncio  # noqa
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from core.database import get_db, Base
from main import app
from fixtures.repositories import database_repository  # noqa
from fixtures.models.user import user, another_user  # noqa

engine = create_async_engine("sqlite+aiosqlite:///:memory:")
async_session = async_sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)


async def override_get_db():
    async with async_session() as session:
        yield session


app.dependency_overrides[get_db] = override_get_db  # noqa


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
