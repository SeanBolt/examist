"""Adding modules.

Revision ID: 009921b01ab6
Revises: 9633df0d8a5e
Create Date: 2016-02-14 20:29:07.398872

"""

# revision identifiers, used by Alembic.
revision = '009921b01ab6'
down_revision = '9633df0d8a5e'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.create_table('module',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('code', sa.String(), nullable=True),
    sa.Column('name', sa.String(), nullable=True),
    sa.Column('institution_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['institution_id'], ['institution.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('user_modules',
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('module_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['module_id'], ['module.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], )
    )
    op.drop_column(u'institution', 'shorthand')
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column(u'institution', sa.Column('shorthand', sa.VARCHAR(), autoincrement=False, nullable=True))
    op.drop_table('user_modules')
    op.drop_table('module')
    ### end Alembic commands ###
