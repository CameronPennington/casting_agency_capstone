import os
from sqlalchemy import Column, String, Integer
from flask_sqlalchemy import SQLAlchemy
import json


db = SQLAlchemy()

SQLALCHEMY_DATABASE_URI = 'postgres://gjvotdgqwslmsd:27a0dd4dffb6901c5833aa51c5cbda6bd1c41e5f417bff11a6eb86d70b617635@ec2-52-73-247-67.compute-1.amazonaws.com:5432/d6d1t6tdju9kei'

def setup_db(app, database_path=SQLALCHEMY_DATABASE_URI):
    app.config['SQLALCHEMY_DATABASE_URI'] = database_path
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

    def format(self):
        return {
            'id': self.id,
            'title': self.title,
            'release_date': self.release_date
        }


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

    def format(self):
        return {
            'id': self.id,
            'name': self.name,
            'age': self.age,
            'gender': self.gender
        }

#maybe add appearances table?