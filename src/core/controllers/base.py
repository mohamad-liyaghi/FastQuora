from typing import Type, Optional
from elasticsearch import NotFoundError
from sqlalchemy.ext.asyncio import AsyncSession
from redis import Redis
from sqlalchemy.orm import DeclarativeBase

from core.database import Base
from core.repositories import DatabaseRepository, RedisRepository, ElasticRepository


class BaseController:
    def __init__(self, model: Type[Base], session: AsyncSession, redis_session: Redis):
        self.model = model
        self.database_repository = DatabaseRepository(model=model, session=session)
        self.redis_repository = RedisRepository(model=model, redis_session=redis_session)
        self.elastic_repository = ElasticRepository(model=model)

    async def create(
        self,
        data: dict,
        cache: bool = False,
        ttl: Optional[int] = 0,
        save_elastic: bool = False,
    ) -> Type[Base]:
        """
        Create a new record in the database (and optionally cache and index it).
        """
        # Create record in the database
        database_record = await self.database_repository.create(data=data)
        data["id"] = database_record.id

        # Optionally cache the record
        await self._cache_record(data, cache, ttl)

        # Optionally index the record
        await self._index_record(data, save_elastic)

        return database_record

    async def retrieve(
        self, is_cached: bool = False, is_indexed: bool = False, **kwargs
    ) -> Type[DeclarativeBase] | DeclarativeBase:
        """
        Retrieve a record from the database (and optionally from cache or index).
        """
        # Attempt to retrieve from cache
        if is_cached:
            record = await self._retrieve_from_cache(kwargs.get("id"))
            if record:
                return record

        # Attempt to retrieve from Elasticsearch
        if is_indexed:
            record = await self._retrieve_from_elastic(kwargs.get("id"))
            if record:
                return record

        # Fallback to retrieve from the database
        record = await self.database_repository.retrieve(**kwargs)
        if record:
            await self._cache_record(record.to_dict(), is_cached)
            await self._index_record(record.to_dict(), is_indexed)

        return record

    async def update(
        self,
        instance: Type[Base],
        data: dict,
        is_cached: bool = False,
        is_indexed: bool = False,
    ) -> Type[Base]:
        """
        Update a record in the database (and optionally in cache and index).
        """
        # Clear the cache and update the index if required
        await self._clear_cache(instance.id, is_cached)
        await self._update_elastic(instance.id, data, is_indexed)

        # Update the record in the database
        return await self.database_repository.update(instance=instance, data=data)

    async def delete(self, instance: Type[Base], is_cached: bool = False, is_indexed: bool = False) -> None:
        """
        Delete a record from the database (and optionally from cache and index).
        """
        # Clear the cache and delete from index if required
        await self._clear_cache(instance.id, is_cached)
        await self._delete_from_elastic(instance.id, is_indexed)

        # Delete the record from the database
        await self.database_repository.delete(instance=instance)

    # Private helper methods
    async def _cache_record(self, data: dict, cache: bool, ttl: Optional[int] = 0):
        if cache:
            await self.redis_repository.create(data=data, ttl=ttl)

    async def _index_record(self, data: dict, save_elastic: bool):
        if save_elastic:
            await self.elastic_repository.create(data=data)

    async def _retrieve_from_cache(self, record_id: int) -> Optional[Type[Base]]:
        record = await self.redis_repository.get(_id=record_id)
        return self.model(**record) if record else None

    async def _retrieve_from_elastic(self, record_id: int) -> DeclarativeBase | None:
        try:
            record = await self.elastic_repository.retrieve(id=record_id)
            return self.model(**record["_source"])
        except NotFoundError:
            return None

    async def _clear_cache(self, record_id: int, is_cached: bool):
        if is_cached:
            await self.redis_repository.delete(_id=record_id)

    async def _update_elastic(self, record_id: int, data: dict, is_indexed: bool):
        if is_indexed:
            await self.elastic_repository.update(id=record_id, data=data)

    async def _delete_from_elastic(self, record_id: int, is_indexed: bool):
        if is_indexed:
            await self.elastic_repository.delete(id=record_id)
