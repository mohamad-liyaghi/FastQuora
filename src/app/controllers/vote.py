from sqlalchemy.ext.asyncio import AsyncSession
from redis import Redis
from app.models import Vote
from core.controllers import BaseController


class VoteController(BaseController):
    def __init__(self, session: AsyncSession, redis_session: Redis):
        self.model = Vote
        super().__init__(model=self.model, session=session, redis_session=redis_session)
