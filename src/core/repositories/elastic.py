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

    async def retrieve(self, id: int) -> dict:
        return await Elastic.get(index=self.model.__tablename__, id=id)
