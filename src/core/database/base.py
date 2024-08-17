from sqlalchemy.orm import declarative_base
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine
from core.settings import settings


Base = declarative_base()
echo = True if settings.DEBUG else False

engine = create_async_engine(settings.POSTGRES_URL, echo=echo, pool_size=10, max_overflow=0)
async_session = async_sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)
