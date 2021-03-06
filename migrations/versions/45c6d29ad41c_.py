"""empty message

Revision ID: 45c6d29ad41c
Revises: 72144f157873
Create Date: 2020-05-14 13:08:17.717637

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '45c6d29ad41c'
down_revision = '72144f157873'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('course',
    sa.Column('course_id', sa.Integer(), nullable=False),
    sa.Column('course_name', sa.String(length=200), nullable=False),
    sa.Column('course_link', sa.String(length=200), nullable=False),
    sa.Column('course_landing_page', sa.String(length=200), nullable=False),
    sa.PrimaryKeyConstraint('course_id')
    )
    op.create_table('recommendation_module',
    sa.Column('id', sa.Integer(), nullable=True),
    sa.Column('course_id', sa.Integer(), nullable=False),
    sa.Column('course_name', sa.String(length=200), nullable=False),
    sa.Column('course_link', sa.String(length=200), nullable=False),
    sa.Column('module_name', sa.String(length=200), nullable=False),
    sa.Column('module_link', sa.String(length=120), nullable=False),
    sa.PrimaryKeyConstraint('course_id')
    )
    op.create_table('student',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('email', sa.String(length=120), nullable=False),
    sa.Column('first_name', sa.String(length=50), nullable=False),
    sa.Column('last_name', sa.String(length=50), nullable=True),
    sa.Column('mobile_number', sa.String(length=10), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email')
    )
    op.create_table('course_module',
    sa.Column('course_id', sa.Integer(), nullable=False),
    sa.Column('module_id', sa.Integer(), nullable=False),
    sa.Column('module_name', sa.String(length=200), nullable=False),
    sa.Column('module_link', sa.String(length=120), nullable=False),
    sa.Column('tags', postgresql.ARRAY(sa.String(), dimensions=1), nullable=True),
    sa.ForeignKeyConstraint(['course_id'], ['course.course_id'], ),
    sa.PrimaryKeyConstraint('module_id')
    )
    op.create_table('questions',
    sa.Column('question_id', sa.Integer(), nullable=False),
    sa.Column('student_id', sa.Integer(), nullable=False),
    sa.Column('course_link', sa.String(length=500), nullable=False),
    sa.Column('answered', sa.String(length=30), nullable=False),
    sa.ForeignKeyConstraint(['student_id'], ['student.id'], ),
    sa.PrimaryKeyConstraint('question_id')
    )
    op.create_table('student_course',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('course_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['course_id'], ['course.course_id'], ),
    sa.ForeignKeyConstraint(['id'], ['student.id'], ),
    sa.PrimaryKeyConstraint('id', 'course_id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('student_course')
    op.drop_table('questions')
    op.drop_table('course_module')
    op.drop_table('student')
    op.drop_table('recommendation_module')
    op.drop_table('course')
    # ### end Alembic commands ###
