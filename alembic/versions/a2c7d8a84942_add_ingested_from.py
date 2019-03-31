"""add ingested from

Revision ID: a2c7d8a84942
Revises: 56a227d5ad00
Create Date: 2019-03-29 18:59:31.311534

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a2c7d8a84942'
down_revision = '56a227d5ad00'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('reddit_post', sa.Column('ingested_from', sa.String(length=40), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###

    op.drop_column('reddit_post', 'ingested_from')
    # ### end Alembic commands ###