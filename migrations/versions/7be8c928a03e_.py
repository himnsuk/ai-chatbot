"""empty message

Revision ID: 7be8c928a03e
Revises: ec6325968919
Create Date: 2020-05-17 21:17:48.094795

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7be8c928a03e'
down_revision = 'ec6325968919'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('course_module', sa.Column('admin_approved', sa.Boolean(), nullable=False))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('course_module', 'admin_approved')
    # ### end Alembic commands ###
