from enum import Enum


class QuestionStatus(Enum):
    OPEN = "open"
    ANSWERED = "answered"
    CLOSED = "closed"
    DELETED = "deleted"
