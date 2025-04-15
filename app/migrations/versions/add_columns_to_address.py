from alembic import op
import sqlalchemy as sa

# Identificadores da revisão
revision = "b9c8d7e6f5a4"
down_revision = None  # Ajuste para a revisão anterior, se houver
branch_labels = None
depends_on = None

def upgrade():
    # Adicionar colunas street_number e complementary à tabela addresses
    op.add_column(
        "address",
        sa.Column("street_number", sa.String, nullable=True)
    )
    op.add_column(
        "address",
        sa.Column("complementary", sa.String, nullable=True)
    )

def downgrade():
    # Remover colunas street_number e complementary
    op.drop_column("address", "street_number")
    op.drop_column("address", "complementary")