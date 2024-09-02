from pydantic import BaseModel
from uuid import UUID


class AnswerCreateRequest(BaseModel):
    content: str
    question_uuid: UUID


class AnswerReplyCreateRequest(BaseModel):
    content: str


class AnswerUpdateRequest(BaseModel):
    content: str
