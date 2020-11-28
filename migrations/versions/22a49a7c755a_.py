"""empty message

Revision ID: 22a49a7c755a
Revises: c6f8921b26ce
Create Date: 2020-05-23 22:14:36.149353

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '22a49a7c755a'
down_revision = 'c6f8921b26ce'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('recommendation_module')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('recommendation_module',
    sa.Column('id', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('course_id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('course_name', sa.VARCHAR(length=200), autoincrement=False, nullable=False),
    sa.Column('course_link', sa.VARCHAR(length=200), autoincrement=False, nullable=False),
    sa.Column('module_name', sa.VARCHAR(length=200), autoincrement=False, nullable=False),
    sa.Column('module_link', sa.VARCHAR(length=120), autoincrement=False, nullable=False),
    sa.PrimaryKeyConstraint('course_id', name='recommendation_module_pkey')
    )
    # ### end Alembic commands ###
