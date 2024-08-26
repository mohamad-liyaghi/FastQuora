from pydantic import BaseModel


class QuestionCreateRequest(BaseModel):
    title: str
    content: str
