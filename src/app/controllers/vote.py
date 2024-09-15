from fastapi import HTTPException
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from redis import Redis
from app.models import Vote
from app.controllers import AnswerController
from core.controllers import BaseController


class VoteController(BaseController):
    def __init__(self, session: AsyncSession, redis_session: Redis):
        self.model = Vote
        super().__init__(model=self.model, session=session, redis_session=redis_session)

    async def create_vote(
        self,
        answer_uuid: UUID,
        user_id: int,
        vote: int,
        answer_controller: AnswerController,
    ) -> dict:
        answer = await answer_controller.retrieve(uuid=answer_uuid)
        if not answer:
            raise HTTPException(status_code=404, detail="Answer not found.")

        if vote_obj := await self.retrieve(user_id=user_id, answer_id=answer.id):
            vote = await self.update(vote_obj, {"vote_type": vote})
        else:
            vote = await self.create(data={"answer_id": answer.id, "user_id": user_id, "vote_type": vote})
        return vote

    async def get_vote(self, answer_id: int, user_id: int):
        cached_result = await self.redis_repository.get(_id=user_id, cache_key=f"vote:{answer_id}:{user_id}")

        if not cached_result:
            database_result = await self.retrieve(user_id=user_id, answer_id=answer_id)

            if database_result:
                await self.redis_repository.create(
                    data=database_result.to_dict(),
                    cache_key=f"vote:{answer_id}:{user_id}",
                )
                return database_result

        return cached_result
