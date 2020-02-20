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
    __tablename__ = 'Movie'

    id = Column(db.Integer, primary_key = True)
    title = Column(db.String(30), nullable = False)
    release_date = Column(db.String(30), nullable = False)

    def __init__(self, title, release_date):
        self.title = title
        self.release_date = release_date


class Actor(db.Model):
    __tablename__ = 'Actor'

    id = Column(db.Integer, primary_key = True)
    name = Column(db.String(30), nullable = False, unique = True)
    age = Column(db.Integer)
    gender = Column(db.String(10))

    def __init__(self, name, age, gender):
        self.name = name
        self.age = age
        self.gender = gender

#maybe add appearances table?