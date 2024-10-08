"""Create questions table

Revision ID: 61a5e108cf59
Revises: 8c1152571ac8
Create Date: 2024-08-26 08:37:41.952431

"""

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql
from uuid import uuid4
from datetime import datetime

# revision identifiers, used by Alembic.
revision = "61a5e108cf59"
down_revision = "8c1152571ac8"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "questions",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("uuid", postgresql.UUID(as_uuid=True), nullable=False, default=uuid4),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("title", sa.String(), nullable=False),
        sa.Column("content", sa.Text(), nullable=False),
        sa.Column("status", sa.String(), nullable=False, default="open"),  # Adjust this based on your enum values
        sa.Column("created_at", sa.DateTime(), nullable=False, default=datetime.now),
        sa.Column("updated_at", sa.DateTime(), nullable=False, default=datetime.now),
        sa.PrimaryKeyConstraint("id", name="questions_pkey"),
        sa.UniqueConstraint("uuid", name="questions_uuid_key"),
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("questions")
    # ### end Alembic commands ###
