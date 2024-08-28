from pydantic import BaseModel
from datetime import datetime


class AnswerCreateResponse(BaseModel):
    content: str
    created_at: datetime


class AnswerUpdateResponse(BaseModel):
    content: str
    updated_at: datetime
