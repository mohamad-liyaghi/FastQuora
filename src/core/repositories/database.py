from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import Type
from core.database import Base


class DatabaseRepository:
    """
    This class is responsible for handling the database operations.
    """

    def __init__(self, model: Type[Base], session: AsyncSession):
        self.model = model
        self.session = session

    async def create(self, data: dict) -> Type[Base]:
        record = self.model(**data)
        self.session.add(record)
        await self.session.commit()
        return record

    async def retrieve(self, **kwargs) -> Type[Base]:
        query = await self.session.execute(select(self.model).filter_by(**kwargs))
        return query.scalars().first()

    async def update(self, instance: Type[Base], data: dict) -> Type[Base]:
        for key, value in data.items():
            setattr(instance, key, value)
        await self.session.commit()
        return instance
