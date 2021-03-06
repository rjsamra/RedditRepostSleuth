"""subconfigchange

Revision ID: a4829f4a5121
Revises: cf449578fbf7
Create Date: 2020-10-10 13:31:17.602780

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a4829f4a5121'
down_revision = 'cf449578fbf7'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('reddit_monitored_sub_config_change',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('updated_at', sa.DateTime(), nullable=False),
    sa.Column('updated_by', sa.String(length=100), nullable=False),
    sa.Column('source', sa.String(length=10), nullable=True),
    sa.Column('subreddit', sa.String(length=200), nullable=False),
    sa.Column('old_value', sa.String(length=2000), nullable=True),
    sa.Column('new_value', sa.String(length=2000), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('subreddit')
    )
    op.create_index('idx_subreddit', 'reddit_monitored_sub_config_change', ['subreddit', 'updated_at'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index('idx_subreddit', table_name='reddit_monitored_sub_config_change')
    op.drop_table('reddit_monitored_sub_config_change')
    # ### end Alembic commands ###
