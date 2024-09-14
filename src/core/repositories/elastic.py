from typing import Type
from core.elastic import Elastic
from core.database import Base


class ElasticRepository:
    """
    This class is responsible for handling the elastic operations.
    """

    def __init__(self, model: Type[Base]):
        self.model = model

    async def create(self, data: dict) -> dict:
        if not data.get("id"):
            raise ValueError("Id is required for elastic search")

        return await Elastic.index(index=self.model.__tablename__, body=data, id=data["id"])

    async def retrieve(self, _id: int) -> dict:
        return await Elastic.get(index=self.model.__tablename__, id=_id)

    async def update(self, _id: int, data: dict) -> dict:
        return await Elastic.update(index=self.model.__tablename__, body={"doc": data}, id=_id)

    async def delete(self, _id: int) -> dict:
        return await Elastic.delete(index=self.model.__tablename__, id=_id)

    async def search(self, query: dict) -> dict:
        return await Elastic.search(index=self.model.__tablename__, body=query)
