from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.schema import PrimaryKeyConstraint
from uuid import UUID, uuid4
from datetime import datetime
from core.database import Base


class User(Base):
    __tablename__ = "users"
    __table_args__ = PrimaryKeyConstraint("id")
    id: Mapped[int]
    uuid: Mapped[UUID] = mapped_column(default_factory=uuid4, unique=True)
    email: Mapped[str] = mapped_column(unique=True)
    nickname: Mapped[str] = mapped_column(unique=True)
    biography: Mapped[str] = mapped_column(max_length=255, default="")
    password: Mapped[str]
    date_joined: Mapped[datetime]

    def __repr__(self) -> str:
        return f"<User {self.email}>"

    def __str__(self) -> str:
        return self.email
