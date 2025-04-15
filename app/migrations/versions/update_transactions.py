from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# Identificadores da revisão
revision = "c3d4e5f6a7b8"
down_revision = "b2c3d4e5f6a7"  # Aponta para webhook_logs

def upgrade():
    # Adicionar colunas à tabela transactions
    op.add_column("transactions", sa.Column("campaign_id", sa.Integer, sa.ForeignKey("campaigns.id"), nullable=True))
    op.add_column("transactions", sa.Column("base_id", sa.Integer, sa.ForeignKey("bases.id"), nullable=True))
    op.add_column("transactions", sa.Column("project_id", sa.Integer, sa.ForeignKey("projects.id"), nullable=True))
    op.add_column("transactions", sa.Column("attendee_id", sa.Integer, sa.ForeignKey("attendees.id"), nullable=True))

def downgrade():
    # Remover colunas de transactions
    op.drop_column("transactions", "attendee_id")
    op.drop_column("transactions", "project_id")
    op.drop_column("transactions", "base_id")
    op.drop_column("transactions", "campaign_id")