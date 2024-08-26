from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.schema import PrimaryKeyConstraint, UniqueConstraint
from uuid import UUID, uuid4
from datetime import datetime
from app.enums.question import QuestionStatus
from core.database import Base


class Question(Base):
    __tablename__ = "questions"
    __table_args__ = (
        PrimaryKeyConstraint("id", name="questions_pkey"),
        UniqueConstraint("uuid", name="questions_uuid_key"),
    )
    id: Mapped[int]
    uuid: Mapped[UUID] = mapped_column(default=uuid4)
    user_id: Mapped[int]
    title: Mapped[str]
    content: Mapped[str]
    status: Mapped[QuestionStatus] = mapped_column(default=QuestionStatus.OPEN.value)
    created_at: Mapped[datetime] = mapped_column(default=datetime.now())
    updated_at: Mapped[datetime] = mapped_column(default=datetime.now())

    def __repr__(self) -> str:
        return f"<Question {self.title}>"

    def __str__(self) -> str:
        return self.title

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "uuid": str(self.uuid),
            "user_id": self.user_id,
            "title": self.title,
            "content": self.content,
            "status": self.status,
            "created_at": str(self.created_at),
            "updated_at": str(self.updated_at),
        }
