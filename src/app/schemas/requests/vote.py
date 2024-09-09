from pydantic import BaseModel
from app.enums.vote import VoteType


class VoteCreateRequest(BaseModel):
    vote: VoteType
