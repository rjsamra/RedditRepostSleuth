"""matchesh found to image search

Revision ID: b2c776dff6e2
Revises: 87d5bc932e2a
Create Date: 2019-11-21 07:34:33.134011

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = 'b2c776dff6e2'
down_revision = '87d5bc932e2a'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('reddit_image_search', 'meme_template_Used')
    op.add_column('reddit_image_search', sa.Column('matches_found', sa.Integer(), nullable=False))
    op.add_column('reddit_image_search', sa.Column('meme_template_used', sa.Integer(), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('reddit_image_search', sa.Column('meme_template_Used', mysql.INTEGER(display_width=11), autoincrement=False, nullable=True))
    op.drop_column('reddit_image_search', 'meme_template_used')
    op.drop_column('reddit_image_search', 'matches_found')
    # ### end Alembic commands ###
