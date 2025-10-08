"""merge produto.ativo + produto_imagem

Revision ID: 3bf777b1b94f
Revises: a70975cafd2b, bd3e08f0e9b2
Create Date: 2025-10-07 19:34:04.684318

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3bf777b1b94f'
down_revision = ('a70975cafd2b', 'bd3e08f0e9b2')
branch_labels = None
depends_on = None


def upgrade():
    pass


def downgrade():
    pass
