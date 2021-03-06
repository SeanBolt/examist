"""Notes table.

Revision ID: ad04219e530a
Revises: 27d9b0a51afe
Create Date: 2016-04-02 00:55:34.398763

"""

# revision identifiers, used by Alembic.
revision = 'ad04219e530a'
down_revision = '27d9b0a51afe'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.create_table('note',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=True),
        sa.Column('question_id', sa.Integer(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.Column('updated_at', sa.DateTime(), nullable=True),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('link', sa.String(), nullable=True),
        sa.Column('file_path', sa.String(), nullable=True),
        sa.ForeignKeyConstraint(['id'], ['entity.id'], ),
        sa.ForeignKeyConstraint(['question_id'], ['question.id'], ),
        sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('note')
    ### end Alembic commands ###
