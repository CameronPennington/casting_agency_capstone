import os
from sqlalchemy import Column, String, Integer
from flask_sqlalchemy import SQLAlchemy
import json


db = SQLAlchemy()

def setup_db(app):
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://postgres:postgres@localhost:5432/casting'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.app = app
    db.init_app(app)

class Movie(db.Model):
    id = Column(db.Integer, primary_key = True)
    title = Column(db.String(30), nullable = False)
    release_date = Column(db.String(30), nullable = False)