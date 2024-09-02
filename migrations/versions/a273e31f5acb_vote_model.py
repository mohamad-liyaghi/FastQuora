"""Vote model

Revision ID: a273e31f5acb
Revises: f1c49bf7b3dd
Create Date: 2024-09-02 08:50:14.910854

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = "a273e31f5acb"
down_revision: Union[str, None] = "f1c49bf7b3dd"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Create votes table
    op.create_table(
        "votes",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("answer_id", sa.Integer(), nullable=False),
        sa.Column("vote_type", sa.String(), nullable=False, server_default="up"),
        sa.Column("uuid", postgresql.UUID(as_uuid=True), nullable=False, unique=True),
        sa.PrimaryKeyConstraint("id", name="votes_pkey"),
        sa.UniqueConstraint("uuid", name="votes_uuid_key"),
    )


def downgrade() -> None:
    # Drop votes table
    op.drop_table("votes")
