import json
from redis import Redis
from typing import Type, Optional
from core.database import Base


class RedisRepository:
    """
    This class is responsible for handling the redis operations.
    """

    def __init__(self, model: Type[Base], redis_session: Redis):
        self.model = model
        self.session = redis_session
        self.base_key = f"{model.__name__}:"

    async def create(self, data: dict, ttl: Optional[int] = None) -> dict:
        """
        Create a new record in the redis
        """
        _id = data.get("id")
        if not _id:
            raise ValueError("id is required")

        await self.session.set(f"{self.base_key}{_id}", json.dumps(data), ex=ttl)
        return data

    async def get(self, _id: int) -> Optional[dict]:
        """
        Get a record from the redis
        """
        data = await self.session.get(f"{self.base_key}{_id}")
        return json.loads(data) if data else None

    async def delete(self, _id: int) -> None:
        """
        Delete a record from the redis
        """
        await self.session.delete(f"{self.base_key}{_id}")
