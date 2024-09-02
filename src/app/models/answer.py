from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.schema import PrimaryKeyConstraint, UniqueConstraint
from uuid import UUID, uuid4
from datetime import datetime
from core.database import Base


class Answer(Base):
    __tablename__ = "answers"
    __table_args__ = (
        PrimaryKeyConstraint("id", name="answers_pkey"),
        UniqueConstraint("uuid", name="answers_uuid_key"),
    )
    id: Mapped[int] = mapped_column(primary_key=True)
    uuid: Mapped[UUID] = mapped_column(default=uuid4, unique=True)
    user_id: Mapped[int] = mapped_column()
    parent_id: Mapped[int] = mapped_column(ForeignKey("answers.id", ondelete="CASCADE"), nullable=True)
    question_id: Mapped[int] = mapped_column(ForeignKey("questions.id", ondelete="CASCADE"))
    content: Mapped[str] = mapped_column()
    is_deleted: Mapped[bool] = mapped_column(default=False)
    created_at: Mapped[datetime] = mapped_column(default=datetime.now())
    updated_at: Mapped[datetime] = mapped_column(default=datetime.now())

    question = relationship("Question", back_populates="answers")

    def __repr__(self) -> str:
        return f"<Answer {self.content}>"

    def __str__(self) -> str:
        return self.content

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "uuid": str(self.uuid),
            "user_id": self.user_id,
            "question_id": self.question_id,
            "content": self.content,
            "is_deleted": self.is_deleted,
            "created_at": str(self.created_at),
            "updated_at": str(self.updated_at),
        }
