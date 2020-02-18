import os
from sqlalchemy import Column, String, Integer
from flask_sqlalchemy import SQLAlchemy
import json

SQLALCHEMY_DATABASE_URI = 'postgres://postgres:postgres@localhost:5432/casting'
SQLALCHEMY_TRACK_MODIFCATIONS = True