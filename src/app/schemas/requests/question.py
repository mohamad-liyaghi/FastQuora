from pydantic import BaseModel


class QuestionCreateRequest(BaseModel):
    title: str
    content: str


class QuestionUpdateRequest(BaseModel):
    title: str
    content: str
