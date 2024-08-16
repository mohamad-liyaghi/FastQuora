from sqlalchemy.ext.asyncio import AsyncSession
from core.database import async_session


async def get_db() -> AsyncSession:
    """Return a database session and close it after use."""
    async with async_session() as session:
        yield session
