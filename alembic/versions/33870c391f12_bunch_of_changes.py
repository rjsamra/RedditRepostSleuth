"""bunch of changes

Revision ID: 33870c391f12
Revises: bdd0f81d7ade
Create Date: 2020-08-29 12:35:42.297993

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '33870c391f12'
down_revision = 'bdd0f81d7ade'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('bot_stat',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('image_reposts_detected', sa.Integer(), nullable=True),
    sa.Column('link_reposts_detected', sa.Integer(), nullable=True),
    sa.Column('private_messages_sent', sa.Integer(), nullable=True),
    sa.Column('comments', sa.Integer(), nullable=True),
    sa.Column('summons_received', sa.Integer(), nullable=True),
    sa.Column('karma_gained', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.add_column('image_reposts', sa.Column('search_id', sa.Integer(), nullable=True))
    op.add_column('image_reposts', sa.Column('source', sa.String(length=100), nullable=True))
    op.add_column('image_reposts', sa.Column('subreddit', sa.String(length=100), nullable=False))
    op.add_column('link_reposts', sa.Column('source', sa.String(length=100), nullable=True))
    op.add_column('link_reposts', sa.Column('subreddit', sa.String(length=100), nullable=False))
    op.add_column('reddit_image_search', sa.Column('subreddit', sa.String(length=100), nullable=False))
    op.add_column('reddit_monitored_sub', sa.Column('check_image_posts', sa.Boolean(), nullable=True))
    op.add_column('reddit_monitored_sub', sa.Column('check_link_posts', sa.Boolean(), nullable=True))
    op.add_column('reddit_monitored_sub', sa.Column('check_text_posts', sa.Boolean(), nullable=True))
    op.add_column('reddit_monitored_sub', sa.Column('check_video_posts', sa.Boolean(), nullable=True))
    op.add_column('reddit_monitored_sub', sa.Column('target_image_match', sa.Integer(), nullable=True))
    op.add_column('reddit_monitored_sub', sa.Column('target_image_meme_match', sa.Integer(), nullable=True))
    op.add_column('reddit_monitored_sub', sa.Column('wiki_managed', sa.Boolean(), nullable=True))
    op.drop_column('reddit_monitored_sub', 'search_depth')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###

    op.add_column('reddit_monitored_sub', sa.Column('search_depth', mysql.INTEGER(), autoincrement=False, nullable=True))
    op.drop_column('reddit_monitored_sub', 'wiki_managed')
    op.drop_column('reddit_monitored_sub', 'target_image_meme_match')
    op.drop_column('reddit_monitored_sub', 'target_image_match')
    op.drop_column('reddit_monitored_sub', 'check_video_posts')
    op.drop_column('reddit_monitored_sub', 'check_text_posts')
    op.drop_column('reddit_monitored_sub', 'check_link_posts')
    op.drop_column('reddit_monitored_sub', 'check_image_posts')
    op.drop_column('reddit_image_search', 'subreddit')
    op.drop_column('link_reposts', 'subreddit')
    op.drop_column('link_reposts', 'source')
    op.drop_column('image_reposts', 'subreddit')
    op.drop_column('image_reposts', 'source')
    op.drop_column('image_reposts', 'search_id')
    op.drop_table('bot_stat')
    # ### end Alembic commands ###
