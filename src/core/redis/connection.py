from redis.asyncio import Redis, ConnectionPool
from core.settings import settings

redis_pool = ConnectionPool.from_url(settings.REDIS_URL, max_connections=100, decode_responses=True)


async def get_redis() -> Redis:
    """
    Return an async Redis instance
    """
    redis = Redis(connection_pool=redis_pool)
    return redis
