from flask import Flask, json

from flask_sqlalchemy import SQLAlchemy

from flask_restful import Api

endpoint = "/dictionary/api"

# Flask Initialization

app = Flask(__name__)

json.provider.DefaultJSONProvider.compact = True
json.provider.DefaultJSONProvider.ensure_ascii = False


# Flask-SQLAlchemy Initialization

app.config["SQLALCHEMY_DATABASE_URI"] = f'mysql+mysqlconnector://root:0123456789@db:3306/dictionary'

db = SQLAlchemy(app)


# Flask-RESTful Initializaiton

import resources as r

api = Api(app)
    
api.add_resource(r.Word, endpoint + "/word")
api.add_resource(r.Words, endpoint + "/words")
api.add_resource(r.Languages, endpoint + "/languages")