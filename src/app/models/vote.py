from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.schema import PrimaryKeyConstraint
from app.enums.vote import VoteType
from core.database import Base


class Vote(Base):
    __tablename__ = "votes"
    __table_args__ = (PrimaryKeyConstraint("id", name="votes_pkey"),)
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column()
    answer_id: Mapped[int] = mapped_column()
    vote_type: Mapped[str] = mapped_column(default=VoteType.UP.value)

    def __repr__(self) -> str:
        return f"<Vote {self.id}>"

    def __str__(self):
        return self.id

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "user_id": self.user_id,
            "answer_id": self.answer_id,
            "vote_type": self.vote_type,
            "source": "database",
        }
