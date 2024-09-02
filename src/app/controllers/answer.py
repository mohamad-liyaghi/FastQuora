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
        if question.status in [
            QuestionStatus.CLOSED.value,
            QuestionStatus.DELETED.value,
        ]:
            raise HTTPException(status_code=400, detail="Question is closed or deleted.")

        data["question_id"] = question.id
        return await self.create(data=data)

    async def update_answer(self, uuid: UUID, data: dict, request_user_id: int) -> Answer:
        answer = await self.retrieve(uuid=uuid, user_id=request_user_id)

        if not answer:
            raise HTTPException(status_code=404, detail="Answer not found.")

        return await self.update(answer, data=data)

    async def delete_answer(self, uuid: UUID, request_user_id: int) -> None:
        answer = await self.retrieve(uuid=uuid)

        if not answer:
            raise HTTPException(status_code=404, detail="Answer not found.")

        if answer.user_id != request_user_id:
            raise HTTPException(status_code=403, detail="You are not allowed to delete this answer.")
        await self.update(answer, data={"is_deleted": True})

    async def create_reply(self, parent_uuid: UUID, data: dict) -> Answer:
        parent = await self.retrieve(uuid=parent_uuid, is_deleted=False, join_fields=["question"])
        if not parent:
            raise HTTPException(status_code=404, detail="Parent answer not found.")

        if parent.question.status in [
            QuestionStatus.CLOSED.value,
            QuestionStatus.DELETED.value,
        ]:
            raise HTTPException(status_code=400, detail="Parent question is closed or deleted.")

        data["parent_id"] = parent.id
        return await self.create(data=data)

    async def retrieve_replies(self, parent_uuid: UUID) -> list[Answer]:
        parent = await self.retrieve(uuid=parent_uuid, is_deleted=False)
        if not parent:
            raise HTTPException(status_code=404, detail="Parent answer not found.")

        return await self.retrieve(parent_id=parent.id, is_deleted=False)
