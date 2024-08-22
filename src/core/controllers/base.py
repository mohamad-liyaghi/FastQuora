from typing import Type, Optional
from elasticsearch import NotFoundError
from core.database import Base
from core.repositories import DatabaseRepository, RedisRepository, ElasticRepository


class BaseController:
    def __init__(self, model, session, redis_session):
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
        if cache:
            await self.redis_repository.create(data=data, ttl=ttl)
        if save_elastic:
            await self.elastic_repository.create(data=data)
        return await self.database_repository.create(data=data)

    async def retrieve(self, is_cached: bool = False, search_elastic: bool = False, **kwargs) -> Type[Base]:
        if is_cached:
            record = await self.redis_repository.get(_id=kwargs.get("id"))
            if record:
                return self.model(**record)
        if search_elastic:
            try:
                record = await self.elastic_repository.retrieve(id=kwargs.get("id"))
                return self.model(**record["_source"])
            except NotFoundError:
                pass
        record = await self.database_repository.retrieve(**kwargs)
        if record:
            await self.redis_repository.create(data=record.to_dict())
        return record

    async def update(
        self,
        instance: Type[Base],
        data: dict,
        is_cached: bool = False,
        is_indexed: bool = False,
    ) -> Type[Base]:
        if is_cached:
            await self.redis_repository.delete(_id=instance.id)

        if is_indexed:
            await self.elastic_repository.update(id=instance.id, data=data)

        return await self.database_repository.update(instance=instance, data=data)

    async def delete(self, instance: Type[Base], is_cached: bool = False, is_indexed: bool = False) -> None:
        if is_cached:
            await self.redis_repository.delete(_id=instance.id)
        if is_indexed:
            await self.elastic_repository.delete(id=instance.id)

        return await self.database_repository.delete(instance=instance)
