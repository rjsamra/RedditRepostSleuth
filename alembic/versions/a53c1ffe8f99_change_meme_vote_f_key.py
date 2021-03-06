"""change meme vote F key

Revision ID: a53c1ffe8f99
Revises: 5111c30c2895
Create Date: 2020-11-20 08:25:42.939220

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a53c1ffe8f99'
down_revision = '5111c30c2895'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('meme_template_potential_votes', sa.Column('meme_template_potential_id', sa.Integer(), nullable=True))

    op.drop_constraint('meme_template_potential_votes_ibfk_1', 'meme_template_potential_votes', type_='foreignkey')
    op.create_foreign_key(None, 'meme_template_potential_votes', 'meme_template_potential', ['meme_template_potential_id'], ['id'])
    op.drop_index('post_id', table_name='meme_template_potential_votes')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'meme_template_potential_votes', type_='foreignkey')
    op.create_foreign_key('meme_template_potential_votes_ibfk_1', 'meme_template_potential_votes', 'meme_template_potential', ['post_id'], ['post_id'])
    op.create_index('post_id', 'meme_template_potential_votes', ['post_id'], unique=True)
    op.drop_column('meme_template_potential_votes', 'meme_template_potential_id')
    # ### end Alembic commands ###
