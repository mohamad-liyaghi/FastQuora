"""Answer model

Revision ID: b88826741b66
Revises: 61a5e108cf59
Create Date: 2024-08-28 09:16:42.845521

"""

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql
from uuid import uuid4
from datetime import datetime

# revision identifiers, used by Alembic.
revision = "b88826741b66"
down_revision = "61a5e108cf59"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "answers",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column(
            "uuid",
            postgresql.UUID(as_uuid=True),
            nullable=False,
            unique=True,
            default=uuid4,
        ),
        sa.Column("user_id", sa.Integer, nullable=False),
        sa.Column("question_id", sa.Integer, nullable=False),
        sa.Column("content", sa.String, nullable=False),
        sa.Column("is_deleted", sa.Boolean, nullable=False, default=False),
        sa.Column("created_at", sa.DateTime, nullable=False, default=datetime.now),
        sa.Column("updated_at", sa.DateTime, nullable=False, default=datetime.now),
        sa.PrimaryKeyConstraint("id", name="answers_pkey"),
        sa.UniqueConstraint("uuid", name="answers_uuid_key"),
    )


def downgrade() -> None:
    op.drop_table("answers")
