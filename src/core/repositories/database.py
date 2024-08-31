from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload

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

    async def retrieve(self, join_fields: list | None = None, **kwargs) -> Type[Base]:
        query = select(self.model)

        if join_fields:
            for field in join_fields:
                query = query.options(selectinload(getattr(self.model, field)))

        query = query.filter_by(**kwargs)
        result = await self.session.execute(query)
        return result.scalars().first()

    async def update(self, instance: Type[Base], data: dict) -> Type[Base]:
        for key, value in data.items():
            setattr(instance, key, value)
        await self.session.commit()
        return instance

    async def delete(self, instance: Type[Base]) -> None:
        await self.session.delete(instance)
        await self.session.commit()
