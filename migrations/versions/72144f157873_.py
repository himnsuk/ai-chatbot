"""empty message

Revision ID: 72144f157873
Revises: 
Create Date: 2020-05-14 12:30:54.331008

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '72144f157873'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('question')
    op.drop_table('course_module')
    op.drop_table('student_course')
    op.drop_table('student')
    op.drop_table('course')
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
    op.create_table('course',
    sa.Column('course_id', sa.INTEGER(), server_default=sa.text("nextval('course_course_id_seq'::regclass)"), autoincrement=True, nullable=False),
    sa.Column('course_name', sa.VARCHAR(length=200), autoincrement=False, nullable=False),
    sa.Column('course_link', sa.VARCHAR(length=200), autoincrement=False, nullable=False),
    sa.Column('course_landing_page', sa.VARCHAR(length=200), autoincrement=False, nullable=False),
    sa.PrimaryKeyConstraint('course_id', name='course_pkey'),
    postgresql_ignore_search_path=False
    )
    op.create_table('student',
    sa.Column('id', sa.INTEGER(), server_default=sa.text("nextval('student_id_seq'::regclass)"), autoincrement=True, nullable=False),
    sa.Column('email', sa.VARCHAR(length=120), autoincrement=False, nullable=False),
    sa.Column('first_name', sa.VARCHAR(length=50), autoincrement=False, nullable=False),
    sa.Column('last_name', sa.VARCHAR(length=50), autoincrement=False, nullable=True),
    sa.Column('mobile_number', sa.VARCHAR(length=10), autoincrement=False, nullable=True),
    sa.PrimaryKeyConstraint('id', name='student_pkey'),
    sa.UniqueConstraint('email', name='student_email_key'),
    postgresql_ignore_search_path=False
    )
    op.create_table('student_course',
    sa.Column('id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('course_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.ForeignKeyConstraint(['course_id'], ['course.course_id'], name='student_course_course_id_fkey'),
    sa.ForeignKeyConstraint(['id'], ['student.id'], name='student_course_id_fkey'),
    sa.PrimaryKeyConstraint('id', 'course_id', name='student_course_pkey')
    )
    op.create_table('course_module',
    sa.Column('course_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('module_id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('module_name', sa.VARCHAR(length=200), autoincrement=False, nullable=False),
    sa.Column('module_link', sa.VARCHAR(length=120), autoincrement=False, nullable=False),
    sa.Column('tags', postgresql.ARRAY(sa.VARCHAR()), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['course_id'], ['course.course_id'], name='course_module_course_id_fkey'),
    sa.PrimaryKeyConstraint('module_id', name='course_module_pkey')
    )
    # ### end Alembic commands ###
