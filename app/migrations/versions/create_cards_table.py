from alembic import op
import sqlalchemy as sa

revision = "b2c3d4e5f6a7"
down_revision = "a1b2c3d4e5f6"
branch_labels = None
depends_on = None

def upgrade():
    op.create_table(
        "cards",
        sa.Column("id", sa.Integer, primary_key=True, index=True),
        sa.Column("maintainer_id", sa.Integer, sa.ForeignKey("maintainers.id"), nullable=False),
        sa.Column("card_id", sa.String, nullable=False)
    )

def downgrade():
    op.drop_table("cards")