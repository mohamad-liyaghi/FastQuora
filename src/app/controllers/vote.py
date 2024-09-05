from sqlalchemy.ext.asyncio import AsyncSession
from redis import Redis
from app.models import Vote
from core.controllers import BaseController


class VoteController(BaseController):
    def __init__(self, session: AsyncSession, redis_session: Redis):
        self.model = Vote
        super().__init__(model=self.model, session=session, redis_session=redis_session)

    async def create_vote(self, answer_id: int, user_id: int, vote: int):
        vote = await self.redis_repository.create(
            data={
                "answer_id": answer_id,
                "user_id": user_id,
                "vote": vote,
                "id": user_id,
            },
            cache_key=f"vote:{answer_id}:{user_id}",
        )
        return vote

    async def get_vote(self, answer_id: int, user_id: int):
        cached_result = await self.redis_repository.get(_id=user_id, cache_key=f"vote:{answer_id}:{user_id}")

        if not cached_result:
            database_result = await self.retrieve(user_id=user_id, answer_id=answer_id)
            if database_result:
                await self.redis_repository.create(data=database_result, cache_key=f"vote:{answer_id}:{user_id}")
                return database_result

        return cached_result
