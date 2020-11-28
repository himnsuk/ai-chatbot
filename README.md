## Setup Guide for AI enabled recommendation chatbot

### 1. Software Setup

For Operating Systems
1. Windows
2. MacOS
3. Linux

Below software list require to pre-install

1. Python 3.5 and above
2. PostgreSQL 12 and above
3. PgAdmin 4 for testing the data and running query result

### 2. Virtual Environment Setup

Here is the [LINK](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/) to install pip on various platform and setting up virtual environment

#### 1. Setting up virtual environment

* For macOS and Linux system
```sh
python -m venv env
```

* For windows
```sh
py -m venv env
```
Activating the virtual environment
* For macOS and Linux
```sh
source env/bin/activate
```
* For windows
```sh
.\env\Scripts\activate
```

### 3. Code Setup

Clone the _**ai-chatbot**_ repository into the already created virtual environment

```sh
git clone https://himnsu@bitbucket.org/ai-chatbot1/ai-chatbot.git
```
Now go to directory by

```sh
cd ai-chatbot
```

To install all the dependencies required to runn the solution run command

```sh
pip install -r requirements.txt
```

create a database with __*chatbot*__ in PostgreSQL with user PostgreSQL which is default.

```sh
CREATE DATABASE chatbot
```

Open the solution in your favorite editor. We have used [__*VSCode*__](https://code.visualstudio.com/) for our complete development.

Now open the file `ai-chatbot/chatbot/__init__.py` file

```sh
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://localhost/chatbot'
```

if you have different username and password you can modify as:

```sh
# Username and password update
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://username:password@localhost/chatbot'
```

### 4. Creating database tables

Open terminal/ command-line and navigate to the chatbot code folder

run command:
```sh
python3
```

it will open python interactive shell. Then run commands

```sh
#1
>>> from chatbot.schemas.model import *
#2
>>> db.create_all()
```
The above commands will generate all the table with relationship required for the database


### 5. Testing with dummy data

To check if everything working end to end populate some 

Open file `dummy_data.py` un-comment the code and run command

```sh
python3 dummy_data.py
```

This will populate dummy data into database

Once data population complete run
```sh
python3 app.py
```
Now go to browser and put the url `http://localhost:5000/`

if the below screens show

![Home Screen](./screen_shots/home-screen.png)

select a student from dropdown and click submit

![Select Student](./screen_shots/submit-selected-student.png)


![Submit Selected Student](./screen_shots/student-selection.png)

after submit you will see screen

![Chatbot Home](./screen_shots/chatbot-home.png)

now submit some query and if it response then things are working fine


### 6. Populating real data with pipeline script

Open file `video_to_tags.py` update variables info

```py
video_file_path = "Video file path from where you want to convert the video"
subscription_key = "Add azure cognitive service subscription key"
```

Then run

```bash
python3 video_to_tags.py
```
It will take around 10-15 minutes of time based on video length selected, by default i have kept it 15 minute which can be change later point of time

After script complete processing it will create tags from the video and insert into database table and also it will create student and course associated with it which can be changed in future

Now open `admin-tag` page by going to url `http://localhost:5000/tags`

![Tag Admin](./screen_shots/tag-admin.png)

On the page you can see two dropdowns

1. Select Course => Couse for which you are trying to generate tags
2. Select Course Module => Modules related to course

These dropdowns will only populate those courses and modules which are not yet approved by administrator 

When you select course and module both the boxes `1). Included Tags and 2. Excluded Tags` will be populated with extracted tags

On the page you can remove the tags and given below input box you can add custom tags.

Once you click submit the course will be ready to access for Students.


### 7. Entity Relationship Diagram

![Entity Relation Diagram](./screen_shots/entity-relationship.jpg)


## _Architecture Diagrams_



### Video to Tag Generation

![Video To Tag Generation](./screen_shots/video-architecture.jpg)



### Student Query Processing

![Student Query Processing](./screen_shots/user-architecture.jpg)


### **Scalability**

The below points will explain how can we further scale the solution:

#### 1. Multiple video processing
As discussed with the team they have multiple video to process daily basis, to solve this issue we can parallelize the video processing pipeline while deploying to any cloud platform (or server)

#### 2. Concurrency management

If chatbot started getting access by multiple user and frequency of query per second increases in this scenario we have to make few changes to solution which is like production-ready web servers like __*Nginx*__, and let your app be handled by WSGI application server like __*Gunicorn*__.


### __*Further Suggestion*__

#### 1. Student registration and course assignment
To achieve this, we can create two pages

1. __*Student Registration Page: -*__ Student can register by providing his details (e.g. Name, email, mobile number) and we can store the information to database

2. __*Admin page for course assignment: -*__ Create an admin page where course can be assigned to registered user

</ul>

#### 2. Dictionary keywords (tags)
We have 3 solution for this which discussed as below:

__*1.	Analyse un-answered questions: -*__ We can analyse the un-answered question by pulling to excel, csv format and check what frequent keywords has been asked from students and we can add to our dictionary database</li>

__*2. Notify only frequent keywords: -*__ As we are storing each query and keyword related to it we can add a threshold mark above which will be useful if same type of tag related query has been asked multiple time you can flag those question and show on dashboard and periodically admin can review and insert into database by admin portal

__*3. Complete automation: -*__ As mentioned in the (b) part of solution we can create a threshold of question. If same type of question has been asked from multiple user. We can create a job which will run periodically and find those keywords and insert into database without any human intervention.

All the above 3 methods will work without issue and next time a student will ask same type of question chatbot will able to answer it.


End of document


~Thank You~

