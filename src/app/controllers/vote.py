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

        vote_instance = await self.redis_repository.create(
            cache_key=f"vote:{answer.id}:{user_id}",
            data={
                "id": answer.id,
                "user_id": user_id,
                "answer_id": answer.id,
                "vote_type": vote,
                "source": "cache",
            },
        )
        return vote_instance

    async def get_vote(self, answer_id: int, user_id: int) -> dict:
        cached_result = await self.redis_repository.get(_id=user_id, cache_key=f"vote:{answer_id}:{user_id}")

        if not cached_result:
            database_result = await self.retrieve(user_id=user_id, answer_id=answer_id)
            dict_result = database_result.to_dict() if database_result else None

            if database_result:
                await self.redis_repository.create(
                    data=database_result.to_dict(),
                    cache_key=f"vote:{answer_id}:{user_id}",
                )
                return dict_result

        return cached_result
