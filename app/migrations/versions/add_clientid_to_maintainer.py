from alembic import op
import sqlalchemy as sa

revision = "a1b2c3d4e5f6"
down_revision = None
branch_labels = None
depends_on = None

def upgrade():
    op.add_column("maintainers", sa.Column("client_id", sa.String, nullable=True))

def downgrade():
    op.drop_column("maintainers", "client_id")