from datetime import datetime
from chatbot import api, app
from flask_restful import reqparse, abort, Api, Resource
from flask import jsonify, render_template, request
from chatbot.schemas.model import *
from chatbot.ml_models.keywords import *
from sqlalchemy import *
import json
import pdb
from flask import Flask,redirect

parser = reqparse.RequestParser()
parser.add_argument('query', type=str)


# API for providing answer to the question
class ChatbotResponse(Resource):
  # Method to store query and extracted tag to Question table
  def writeQuestionWithAnswer(self, student_id, question, answered, extracted_keywords):
    quest = Question(student_id=student_id, answered=answered, question=question,
             created_date=datetime.datetime.now(), extracted_tags=extracted_keywords)
    db.session.add(quest)
    db.session.commit()
  
  def highest_n_gram_recommendation(self, recommended_modules, extracted_keyword_dict):
    keys_of_dict = ["five-gram", "four-gram", "tri-gram", "bi-gram"]
    rec_mod = []
    for module in recommended_modules:
      for n_gram in keys_of_dict:
        if(all(x in module["tags"] for x in extracted_keyword_dict[n_gram] ) and (module not in rec_mod)):
          rec_mod.append(module)

    if len(rec_mod) > 2:
      return rec_mod[:2]
    else:
      return rec_mod
          



  def post(self):
    json_data = request.get_json()
    question_asked = json_data['query']
    student_id = json_data['student_id']
    extracted_keywords_tuple = extract_keyword(json_data['query'])
    extracted_keywords = ','.join(extracted_keywords_tuple[0])
    extracted_keyword_dict = extracted_keywords_tuple[1]
    print(extracted_keywords)
    formatted_query = "'{" + f'{extracted_keywords}' + "}'"

    modules_with_keyword = CourseModule.query\
      .join(Course, CourseModule.module_course)\
      .filter(CourseModule.tags.op('&&')('{' + f'{extracted_keywords}'+'}'))\
      .subquery()

    course_subscribed_by_student = Course.query\
      .join(Student, Course.subscribed_by)\
      .filter(Student.id == student_id)\
      .subquery()

    student_recommendation_modules = db.session.query(modules_with_keyword).join(course_subscribed_by_student).all()
    if student_recommendation_modules:
      recommended_modules = course_modules_schema.dump(student_recommendation_modules)
      if len(recommended_modules) > 1:
        rec_mod = self.highest_n_gram_recommendation(recommended_modules, extracted_keyword_dict)
        if rec_mod:
          recommended_modules = rec_mod

      self.writeQuestionWithAnswer(student_id, question_asked, "yes", extracted_keywords)
      return {"recommended_modules": recommended_modules}

    else:
      recommended_course = []
      modules_with_keyword_subquery = CourseModule.query \
        .with_entities(CourseModule.course_id, CourseModule.module_name, CourseModule.module_link) \
        .filter(CourseModule.tags.op('&&')('{' + f'{extracted_keywords}'+'}')).subquery()
      course_list_with_modules = db.session.query(Course, modules_with_keyword_subquery) \
        .join(modules_with_keyword_subquery, and_(Course.course_id == modules_with_keyword_subquery.c.course_id)).all()


      if course_list_with_modules:
        for course in course_list_with_modules:
          if course[0] not in recommended_course:
            recommended_course.append(course[0])

        course_list_dict = courses_schema.dump(recommended_course)
        self.writeQuestionWithAnswer(student_id, question_asked, "found in other course", extracted_keywords)
        return {"recommended_course": course_list_dict}
      else:
        self.writeQuestionWithAnswer(
          student_id, question_asked, "no", extracted_keywords)
        return {"data_not_available_in_db": "Data not available in db"}


class StudentCourse(Resource):
  def get(self, student_id):
    student_subscription_list = Student.query.filter_by(
      id=student_id).first()
    course_list = student_subscription_list.subscription
    course_list_json = courses_schema.dump(course_list)
    return course_list_json


class PendingModulesTag(Resource):
  def get(self, course_id):
    modules = CourseModule.query.filter_by(course_id = course_id).all()
    modules_list_json = course_modules_schema.dump(modules)
    return modules_list_json


class UpdateModuleWithCorrectTag(Resource):
  def post(self):
    json_data = request.get_json()
    module = CourseModule.query.filter_by(module_id = json_data['module_id']).first()
    module.tags = json_data['included_tags'].split(",")
    module.excluded_tags = json_data['excluded_tags'].split(",")
    module.admin_approved = True
    module.generated_tags = []
    db.session.commit()
    return {"key": "Success"}


api.add_resource(PendingModulesTag, '/modules/<string:course_id>')
api.add_resource(ChatbotResponse, '/chatbot')
api.add_resource(StudentCourse, '/student-subscription/<string:student_id>')
api.add_resource(UpdateModuleWithCorrectTag, '/update-module')


@app.route("/")
def home():
  students_list = Student.query.with_entities(
    Student.first_name, Student.last_name, Student.id).all()
  return render_template("index.html", students_list=students_list)


@app.route("/chatbot")
def chatbot():
  return render_template("chatbot.html")


@app.route("/admin")
def admin_page():
  question_list = Question.query.all()
  return render_template("admin.html", question_list=question_list)


@app.route("/tags")
def admin_tags():
  course_list_with_pending_tags_approval = Course.query.with_entities(Course.course_id, Course.course_name)\
    .join(CourseModule, Course.course_modules)\
    .filter(CourseModule.admin_approved == False)\
    .distinct()\
    .all()
  return render_template("admin_tags.html", courses=course_list_with_pending_tags_approval)
