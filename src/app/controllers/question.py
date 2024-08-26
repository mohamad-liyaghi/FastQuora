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

    async def delete_question(self, uuid: UUID, user_id: int) -> None:
        question = await self.retrieve_by_uuid(uuid=uuid)

        if not question:
            raise HTTPException(status_code=404, detail="Question not found")

        if question.user_id != user_id:
            raise HTTPException(status_code=403, detail="Forbidden")

        await self.delete(question)
        return

    async def update_question(self, uuid: UUID, data: dict, user_id: int) -> Question:
        question = await self.retrieve_by_uuid(uuid=uuid)

        if not question:
            raise HTTPException(status_code=404, detail="Question not found")

        if question.user_id != user_id:
            raise HTTPException(status_code=403, detail="Forbidden")

        return await self.update(question, data=data)
