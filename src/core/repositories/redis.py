from typing import Type
from core.database import Base
from redis import Redis


class RedisRepository:
    """
    This class is responsible for handling the redis operations.
    """

    def __init__(self, model: Type[Base], redis_session: Redis):
        self.model = model
        self.session = redis_session
