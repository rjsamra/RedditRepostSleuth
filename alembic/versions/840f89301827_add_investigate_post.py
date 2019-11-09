"""add investigate post

Revision ID: 840f89301827
Revises: 5ca77ffdd9bf
Create Date: 2019-11-05 07:48:48.242526

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '840f89301827'
down_revision = '5ca77ffdd9bf'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('investigate_post',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('post_id', sa.String(length=100), nullable=False),
    sa.Column('matches', sa.Integer(), nullable=True),
    sa.Column('found_at', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('post_id')
    )
    op.drop_index('post_id', table_name='reddit_post_reply')
    op.drop_index('reply_id', table_name='reddit_post_reply')
    op.drop_table('reddit_post_reply')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('reddit_post_reply',
    sa.Column('id', mysql.INTEGER(display_width=11), autoincrement=True, nullable=False),
    sa.Column('post_id', mysql.VARCHAR(length=100), nullable=False),
    sa.Column('reply_id', mysql.VARCHAR(length=100), nullable=True),
    sa.Column('reply_body', mysql.VARCHAR(charset='utf8mb4', length=1000), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    mysql_default_charset='utf8',
    mysql_engine='InnoDB'
    )
    op.create_index('reply_id', 'reddit_post_reply', ['reply_id'], unique=True)
    op.create_index('post_id', 'reddit_post_reply', ['post_id'], unique=True)
    op.drop_table('investigate_post')
    # ### end Alembic commands ###