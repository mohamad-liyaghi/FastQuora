from sqlalchemy.ext.asyncio import AsyncSession
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

    async def update(self, record: Type[Base], data: dict) -> Type[Base]:
        for key, value in data.items():
            setattr(record, key, value)
        await self.session.commit()
        return record
