from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.schema import PrimaryKeyConstraint, UniqueConstraint
from uuid import UUID, uuid4
from datetime import datetime
from core.database import Base


class User(Base):
    __tablename__ = "users"
    __table_args__ = (
        PrimaryKeyConstraint("id", name="users_pkey"),
        UniqueConstraint("uuid", name="users_uuid_key"),
        UniqueConstraint("email", name="users_email_key"),
        UniqueConstraint("nickname", name="users_nickname_key"),
    )
    id: Mapped[int]
    uuid: Mapped[UUID] = mapped_column(default=uuid4)
    email: Mapped[str]
    nickname: Mapped[str]
    biography: Mapped[str] = mapped_column(default="")
    password: Mapped[str]
    date_joined: Mapped[datetime] = mapped_column(default=datetime.now())

    def __repr__(self) -> str:
        return f"<User {self.email}>"

    def __str__(self) -> str:
        return self.email
