# README

This repository is for ai-chatbot recommendation system

#### To install all the requirements run below command

- pip install -r requirements.txt
  or
- conda install -r requirements.txt

### Migration of database

- python3 manage.py db migrate

- python3 manage.py db upgrade

### In case of reset index of question table

ALTER SEQUENCE question_question_id_seq RESTART WITH 1

### Postgres command linux-manjaro

- sudo systemctl status postgresql
- sudo systemctl start postgresql
- sudo systemctl status postgresql

### Below code used for populating dummy data into database but while pushing data directly from dataframe to table datatypes are getting changed

```py
course_list = pd.read_csv("./csv-files/course.csv")
course_list['created_time'] = datetime.now()
print(course_list)
course_list.to_sql("course", db.engine, if_exists = "append", index = False)


def extract_arr(tags):
    extracted_tag_list = tags.replace("}", "").replace("{", "").replace('"', '').split(",")
    return extracted_tag_list

course_module = pd.read_csv("./csv-files/CourseModule.csv")
course_module["tags"] = course_module["tags"].apply(lambda tags: extract_arr(tags))
course_module["created_time"] = datetime.now()
course_module["admin_approved"] = False
course_module.to_sql("course_module", db.engine, if_exists = "replace", index = False)

student = pd.read_csv("./csv-files/students.csv")
student["created_time"] = datetime.now()
student.to_sql("student", db.engine, if_exists = "append", index = False)

student_course = pd.read_csv("./csv-files/id_coure_id.csv")
student_course.to_sql("student_course", db.engine, if_exists = "append", index = False)
```

### This was the initial query for fetching the modules which got updated in further iteration

```sql
select A.id, A.course_id, A.course_name, A.course_link, B.module_name, B.module_link from
    (select S.id, C.course_id, C.course_name, C.course_link, C.course_landing_page
    from student as S
    join student_course as SC on S.id = SC.id
    join course as C on SC.course_id = C.course_id
    where S.id = {student_id}) as A
    join
    (select *
    from public.course_module
    WHERE tags && {formatted_query}) as B
    on A.course_id = B.course_id
```

#### Python Code

```py
create_query = f"""select A.id, A.course_id, A.course_name, A.course_link, B.module_name, B.module_link from
                    (select S.id, C.course_id, C.course_name, C.course_link, C.course_landing_page
                    from student as S
                    join student_course as SC on S.id = SC.id
                    join course as C on SC.course_id = C.course_id
                    where S.id = {student_id}) as A
                    join
                    (select *
                    from public.course_module
                    WHERE tags && {formatted_query}) as B
                    on A.course_id = B.course_id"""

student_recommendation_modules = db.engine.execute(create_query)
```
