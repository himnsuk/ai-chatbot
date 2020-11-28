from flask import Flask
from flask_restful import reqparse, abort, Api, Resource
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_marshmallow import Marshmallow

app = Flask(__name__)
CORS(app)
api = Api(app)

app.config["DEBUG"] = True

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://localhost/chatbot'

db = SQLAlchemy(app)
ma = Marshmallow(app)

from chatbot import routes