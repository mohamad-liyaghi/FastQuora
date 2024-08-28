from pydantic import BaseModel
from uuid import UUID


class AnswerCreateRequest(BaseModel):
    content: str
    question_uuid: UUID


class AnswerUpdateRequest(BaseModel):
    content: str
