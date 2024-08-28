from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException
from uuid import UUID
from redis import Redis
from app.enums.question import QuestionStatus
from app.controllers import QuestionController
from app.models import Answer
from core.controllers import BaseController


class AnswerController(BaseController):
    def __init__(self, session: AsyncSession, redis_session: Redis):
        self.model = Answer
        super().__init__(model=self.model, session=session, redis_session=redis_session)

    async def create_answer(self, question_controller: QuestionController, question_uuid: UUID, data: dict) -> Answer:
        question = await question_controller.retrieve_by_uuid(uuid=question_uuid)
        if question.status in [QuestionStatus.CLOSED, QuestionStatus.DELETED]:
            raise HTTPException(status_code=400, detail="Question is closed or deleted.")

        data["question_id"] = question.id
        return await self.create(data=data)
