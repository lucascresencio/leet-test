from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# Identificadores da revisão
revision = "d4e5f6a7b8c9"
down_revision = None  # Ajuste para apontar para a migração anterior, se existir

def upgrade():
    # Criar enums
    op.execute("CREATE TYPE payment_method AS ENUM ('credit_card', 'boleto', 'pix')")
    op.execute("CREATE TYPE transaction_status AS ENUM ('pending', 'paid', 'failed', 'canceled', 'expired')")

    # Criar tabela cards
    op.create_table(
        "cards",
        sa.Column("id", sa.Integer, primary_key=True, index=True),
        sa.Column("maintainer_id", sa.Integer, sa.ForeignKey("maintainers.id"), nullable=False),
        sa.Column("card_id", sa.String, nullable=False, unique=True),
        sa.Column("last_four_digits", sa.String(4), nullable=False),
        sa.Column("brand", sa.String, nullable=False),
        sa.Column("status", sa.String, nullable=False),
        sa.Column("created_at", sa.DateTime, nullable=False, server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime, nullable=False, server_default=sa.func.now())
    )

    # Criar tabela transactions
    op.create_table(
        "transactions",
        sa.Column("id", sa.Integer, primary_key=True, index=True),
        sa.Column("maintainer_id", sa.Integer, sa.ForeignKey("maintainers.id"), nullable=False),
        sa.Column("ong_id", sa.Integer, sa.ForeignKey("ongs.id"), nullable=False),
        sa.Column("campaign_id", sa.Integer, sa.ForeignKey("campaigns.id"), nullable=True),
        sa.Column("base_id", sa.Integer, sa.ForeignKey("bases.id"), nullable=True),
        sa.Column("project_id", sa.Integer, sa.ForeignKey("projects.id"), nullable=True),
        sa.Column("attendee_id", sa.Integer, sa.ForeignKey("attendees.id"), nullable=True),
        sa.Column("amount", sa.Float, nullable=False),
        sa.Column("commission_amount", sa.Float, nullable=False),
        sa.Column("payment_method", postgresql.ENUM("credit_card", "boleto", "pix", name="payment_method"), nullable=False),
        sa.Column("status", postgresql.ENUM("pending", "paid", "failed", "canceled", "expired", name="transaction_status"), nullable=False),
        sa.Column("order_id", sa.String, nullable=True),
        sa.Column("charge_id", sa.String, nullable=True),
        sa.Column("card_id", sa.String, nullable=True),
        sa.Column("boleto_url", sa.String, nullable=True),
        sa.Column("boleto_barcode", sa.String, nullable=True),
        sa.Column("pix_qr_code", sa.String, nullable=True),
        sa.Column("pix_code", sa.String, nullable=True),
        sa.Column("error_message", sa.String, nullable=True),
        sa.Column("created_at", sa.DateTime, nullable=False, server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime, nullable=False, server_default=sa.func.now())
    )

    # Criar tabela webhook_logs
    op.create_table(
        "webhook_logs",
        sa.Column("id", sa.Integer, primary_key=True, index=True),
        sa.Column("event", sa.String, nullable=False),
        sa.Column("payload", postgresql.JSON, nullable=False),
        sa.Column("received_at", sa.DateTime, nullable=False, server_default=sa.func.now())
    )

    # Adicionar commission_rate à tabela ongs
    op.add_column(
        "ongs",
        sa.Column("commission_rate", sa.Float, nullable=False, server_default="0.04")
    )

def downgrade():
    # Remover commission_rate
    op.drop_column("ongs", "commission_rate")

    # Remover tabelas
    op.drop_table("webhook_logs")
    op.drop_table("transactions")
    op.drop_table("cards")

    # Remover enums
    op.execute("DROP TYPE transaction_status")
    op.execute("DROP TYPE payment_method")