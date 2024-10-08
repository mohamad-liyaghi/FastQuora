from pydantic import BaseModel
from app.enums.question import QuestionStatus
from datetime import datetime
from app.schemas.responses.answer import AnswerResponse


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
    answers: list[AnswerResponse]


class QuestionUpdateResponse(BaseQuestionResponse):
    ...
