# -*- encoding: utf-8 -*-
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager


app = Flask(__name__, static_folder="static")
lm = LoginManager(app)
app.config.from_object('app.configuration.DevelopmentConfig')

db = SQLAlchemy(app)  # flask-sqlalchemy


from app import views, models
