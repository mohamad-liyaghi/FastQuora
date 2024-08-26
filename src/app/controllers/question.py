from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID
from redis import Redis
from app.models import Question
from core.controllers import BaseController


class QuestionController(BaseController):
    def __init__(self, session: AsyncSession, redis_session: Redis):
        self.model = Question
        super().__init__(model=self.model, session=session, redis_session=redis_session)

    async def retrieve_by_uuid(self, uuid: UUID) -> Question:
        question = await self.retrieve(uuid=uuid)
        if not question:
            raise HTTPException(status_code=404, detail="Question not found")
        return question
