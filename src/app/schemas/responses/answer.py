from pydantic import BaseModel
from datetime import datetime
from uuid import UUID


class AnswerResponse(BaseModel):
    uuid: UUID
    content: str
    created_at: datetime
    updated_at: datetime


class AnswerCreateResponse(BaseModel):
    content: str
    created_at: datetime


class AnswerUpdateResponse(BaseModel):
    content: str
    updated_at: datetime
