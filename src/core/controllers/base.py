from typing import Type
from core.database import Base
from core.repositories import DatabaseRepository


class BaseController:
    def __init__(self, model, session):
        self.model = model
        self.database_repository = DatabaseRepository(model=model, session=session)

    async def create(self, data: dict) -> Type[Base]:
        return await self.database_repository.create(data=data)

    async def retrieve(self, **kwargs) -> Type[Base]:
        return await self.database_repository.retrieve(**kwargs)

    async def update(self, instance: Type[Base], data: dict) -> Type[Base]:
        return await self.database_repository.update(instance=instance, data=data)

    async def delete(self, instance: Type[Base]) -> None:
        return await self.database_repository.delete(instance=instance)
