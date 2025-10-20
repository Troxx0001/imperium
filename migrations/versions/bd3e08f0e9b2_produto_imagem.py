"""Add produto_imagem table"""

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'bd3e08f0e9b2'
down_revision = '7cd409af3585'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'produto_imagem',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('produto_id', sa.Integer(), nullable=False),
        sa.Column('filename', sa.String(length=255), nullable=False),
        sa.Column('ordem', sa.Integer(), nullable=False, server_default='0'),
        sa.ForeignKeyConstraint(['produto_id'], ['produto.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )


def downgrade():
    op.drop_table('produto_imagem')
