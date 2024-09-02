"""Parent Id field

Revision ID: f1c49bf7b3dd
Revises: b88826741b66
Create Date: 2024-09-02 07:35:36.836955

"""

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = "f1c49bf7b3dd"
down_revision = "b88826741b66"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column("answers", sa.Column("parent_id", sa.Integer(), nullable=True))
    op.create_foreign_key(
        "fk_answers_parent_id_answers",
        "answers",
        "answers",
        ["parent_id"],
        ["id"],
        ondelete="CASCADE",
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint("fk_answers_parent_id_answers", "answers", type_="foreignkey")
    op.drop_column("answers", "parent_id")
    # ### end Alembic commands ###