"""iamge search update

Revision ID: 505caf95a77e
Revises: c8f1e18b7ebc
Create Date: 2021-02-21 11:25:47.481725

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '505caf95a77e'
down_revision = 'c8f1e18b7ebc'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index('comment_id', table_name='reddit_comments')
    op.drop_index('idx_comment_hash', table_name='reddit_comments')
    op.drop_index('idx_comment_id', table_name='reddit_comments')
    op.drop_table('reddit_comments')
    op.add_column('reddit_image_search', sa.Column('filter_crossposts', sa.Boolean(), nullable=True))
    op.add_column('reddit_image_search', sa.Column('filter_same_author', sa.Boolean(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('reddit_image_search', 'filter_same_author')
    op.drop_column('reddit_image_search', 'filter_crossposts')
    op.create_table('reddit_comments',
    sa.Column('id', mysql.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('comment_id', mysql.VARCHAR(length=100), nullable=False),
    sa.Column('body', mysql.TEXT(charset='utf8mb4', collation='utf8mb4_general_ci'), nullable=True),
    sa.Column('ingested_at', mysql.DATETIME(), nullable=True),
    sa.Column('text_hash', mysql.VARCHAR(length=32), nullable=True),
    sa.Column('perma_link', mysql.VARCHAR(length=300), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    mysql_default_charset='utf8',
    mysql_engine='InnoDB',
    mysql_row_format='COMPRESSED'
    )
    op.create_index('idx_comment_id', 'reddit_comments', ['comment_id'], unique=False)
    op.create_index('idx_comment_hash', 'reddit_comments', ['text_hash'], unique=False)
    op.create_index('comment_id', 'reddit_comments', ['comment_id'], unique=True)
    # ### end Alembic commands ###