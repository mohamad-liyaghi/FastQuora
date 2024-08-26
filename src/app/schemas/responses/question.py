from pydantic import BaseModel
from app.enums.question import QuestionStatus
from datetime import datetime


class BaseQuestionResponse(BaseModel):
    id: int
    title: str
    content: str
    status: QuestionStatus
    created_at: datetime
    updated_at: datetime


class QuestionCreateResponse(BaseQuestionResponse):
    ...


class QuestionRetrieveResponse(BaseQuestionResponse):
    ...
