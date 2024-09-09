from pydantic import BaseModel
from app.enums.vote import VoteType


class VoteCreateResponse(BaseModel):
    vote: VoteType
