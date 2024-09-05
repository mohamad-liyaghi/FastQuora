from sqlalchemy.ext.asyncio import AsyncSession
from redis import Redis
from app.models import Vote
from core.controllers import BaseController


class VoteController(BaseController):
    def __init__(self, session: AsyncSession, redis_session: Redis):
        self.model = Vote
        super().__init__(model=self.model, session=session, redis_session=redis_session)

    async def create_vote(self, question_id: int, user_id: int, vote: int):
        vote = await self.redis_repository.create(
            data={
                "question_id": question_id,
                "user_id": user_id,
                "vote": vote,
                "id": user_id,
            },
            cache_key=f"vote:{question_id}:{user_id}",
        )
        return vote
