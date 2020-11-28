from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://localhost/chatbot'

db = SQLAlchemy(app)

from chatbot.schemas.model import *

migrate = Migrate(app, db)

manager = Manager(app)
manager.add_command('db', MigrateCommand)



if __name__ == '__main__':
    manager.run()