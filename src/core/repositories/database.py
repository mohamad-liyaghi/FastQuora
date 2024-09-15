from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from sqlalchemy.orm.exc import NoResultFound
from typing import Type, List, Optional, TypeVar, Union, cast
from sqlalchemy.engine import Result
from core.database import Base

T = TypeVar("T", bound=Base)


class DatabaseRepository:
    """
    This class is responsible for handling the database operations.
    """

    def __init__(self, model: Type[T], session: AsyncSession):
        self.model = model
        self.session = session

    async def create(self, data: dict) -> T:
        record = self.model(**data)
        self.session.add(record)
        await self.session.commit()
        return record

    async def bulk_create(self, data: List[dict]) -> List[T]:
        if not data:
            raise ValueError("Data cannot be empty")
        records = [self.model(**record) for record in data]
        self.session.add_all(records)
        await self.session.commit()
        return records

    async def retrieve(
        self, join_fields: Optional[List[str]] = None, many: bool = False, **kwargs
    ) -> Union[T, List[T], None]:
        query = select(self.model)

        if join_fields:
            for field in join_fields:
                query = query.options(selectinload(getattr(self.model, field)))

        query = query.filter_by(**kwargs)
        result: Result = await self.session.execute(query)

        if many:
            # Explicitly casting the result to List[T]
            return cast(List[T], result.scalars().all())
        else:
            try:
                # Explicitly casting the result to T
                return cast(T, result.scalars().first())
            except NoResultFound:
                return

    async def update(self, instance: T, data: dict) -> T:
        for key, value in data.items():
            setattr(instance, key, value)
        await self.session.commit()
        return instance

    async def delete(self, instance: T) -> None:
        await self.session.delete(instance)
        await self.session.commit()
