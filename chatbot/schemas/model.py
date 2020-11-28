
from chatbot import db, ma
import datetime
from sqlalchemy import  DateTime
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy import String, JSON
from sqlalchemy.orm import joinedload, subqueryload, aliased

student_course = db.Table('student_course',
              db.Column('id', db.Integer, db.ForeignKey(
                'student.id'), primary_key=True),
              db.Column('course_id', db.Integer, db.ForeignKey(
                'course.course_id'), primary_key=True)
              )


class Student(db.Model):
  id = db.Column(db.Integer, primary_key=True, autoincrement=True)
  email = db.Column(db.String(120), unique=True, nullable=False)
  first_name = db.Column(db.String(50), nullable=False)
  last_name = db.Column(db.String(50))
  mobile_number = db.Column(db.String(10))
  created_time = db.Column(DateTime, default=datetime.datetime.utcnow)
  subscription = db.relationship(
    'Course', secondary=student_course, lazy='subquery', backref=db.backref('students', lazy=True))
  student_question = db.relationship(
    'Question', backref='student', lazy=True)


class StudentSchema(ma.Schema):
  class Meta:
    fields = ('id', 'email', 'first_name', 'last_name', 'mobile_number')


student_schema = StudentSchema()
students_schema = StudentSchema(many=True)


class Course(db.Model):
  course_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
  course_name = db.Column(db.String(200), nullable=False)
  course_link = db.Column(db.String(200), nullable=False)
  course_landing_page = db.Column(db.String(200), nullable=False)
  created_time = db.Column(DateTime, default=datetime.datetime.utcnow)
  course_modules = db.relationship(
    'CourseModule', backref='course', lazy=True)
  subscribed_by = db.relationship(
    'Student', secondary=student_course, lazy='subquery', backref=db.backref('courses', lazy=True))


class CourseSchema(ma.Schema):
  class Meta:
    fields = ('course_id', 'course_name',
          'course_link', 'course_landing_page')


course_schema = CourseSchema()
courses_schema = CourseSchema(many=True)


class CourseModule(db.Model):
  course_id = db.Column(db.Integer, db.ForeignKey(
    'course.course_id'), nullable=False)
  module_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
  module_name = db.Column(db.String(200), nullable=False)
  module_link = db.Column(db.String(120), nullable=False)
  tags = db.Column(ARRAY(String, dimensions=1))
  generated_tags = db.Column(ARRAY(String, dimensions=1))
  excluded_tags = db.Column(ARRAY(String, dimensions=1))
  admin_approved = db.Column(db.Boolean, nullable = False)
  created_time = db.Column(DateTime, default=datetime.datetime.utcnow)
  module_course = db.relationship(
    'Course', backref='coursemodule', lazy=True)


class CourseModuleSchema(ma.Schema):
  class Meta:
    fields = ('course_id', 'module_id',
          'module_name', 'module_link', 'tags', 'generated_tags', 'excluded_tags')


course_module_schema = CourseModuleSchema()
course_modules_schema = CourseModuleSchema(many=True)

class Question(db.Model):
  question_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
  student_id = db.Column(db.Integer, db.ForeignKey(
    'student.id'), nullable=False)
  question = db.Column(db.String(1000), nullable=False)
  answered = db.Column(db.String(30), nullable=False)
  extracted_tags = db.Column(db.String(500))
  created_date = db.Column(DateTime, default=datetime.datetime.utcnow)


class QuestionSchema(ma.Schema):
  class Meta:
    fields = ('question_id', 'student_id', 'answered')


question_module_schema = QuestionSchema()
question_modules_schema = QuestionSchema(many=True)
