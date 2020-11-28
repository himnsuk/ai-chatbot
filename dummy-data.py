from chatbot.schemas.model import *
from datetime import datetime
import pandas as pd
import pdb
import csv
from random import randrange

# First Delete all data
# delete_question_table = Question.query.delete()
# delete_course_module_table = CourseModule.query.delete()
# delete_course_table = Course.query.delete()
# delete_student_table = Student.query.delete()

# Add data to table
# with open("./csv-files/students.csv") as students_file:
#   students = csv.reader(students_file, delimiter=",")
#   next(students)
#   for row in students:
#     stu = Student(email = row[1], first_name = row[2], last_name = row[3], mobile_number = row[4], created_time = datetime.now())
#     db.session.add(stu)
#   db.session.commit()

# with open("./csv-files/course.csv") as course_file:
#   courses = csv.reader(course_file, delimiter=",")
#   next(courses)
#   for row in courses:
#     course = Course(course_name = row[1], course_link = row[2], course_landing_page = row[3], created_time = datetime.now())
#     # print(row)
#     # print(course)
#     db.session.add(course)
#   db.session.commit()

# # Adding many to many relationship between Student and Course
# students = Student.query.all()
# courses = Course.query.all()
# len_course = len(courses)
# for student in students:
#   student.subscription.append(courses[randrange(len_course)])
#   db.session.commit()

# # Adding one to many relationship between Course and CourseModule
# with open("./csv-files/CourseModule.csv") as course_module_file:
#   course_modules = csv.reader(course_module_file, delimiter=",")
#   next(course_modules)
#   for row in course_modules:
#     row[4] = row[4].replace("}", "").replace("{", "").replace('"', '').split(",")
#     row[5] = row[5].replace("}", "").replace("{", "").replace('"', '').split(",")
#     row[6] = row[6].replace("}", "").replace("{", "").replace('"', '').split(",")
#     course_module = CourseModule(module_name = row[2], module_link = row[3], tags = row[4], excluded_tags = row[5], generated_tags = row[6], admin_approved = False, created_time = datetime.now())
#     courses[randrange(len_course)].course_modules.append(course_module)
#     db.session.commit()