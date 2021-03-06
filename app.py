import os
import json
from flask import Flask, request, abort, jsonify
from sqlalchemy import exc
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from models import db, setup_db, Movie, Actor
from auth import requires_auth

def create_app(test_config=None):
  # create and configure the app
  app = Flask(__name__)
  setup_db(app)
  CORS(app)
  return app

APP = create_app()

@APP.route('/movies', methods=['POST'])
@requires_auth('post:movies')
def create_movie(token):

  req_data = request.get_json()
  if 'title' not in req_data or 'release_date' not in req_data:
    abort(422)
  title = req_data['title']
  release_date = req_data['release_date']

  new_movie = Movie( title=title, release_date = release_date)

  db.session.add(new_movie)
  db.session.commit()

  db.session.close()
  return jsonify({
    'success': True
  }), 201

@APP.route('/actors', methods=['POST'])
@requires_auth('post:actors')
def create_actor(token):

  req_data = request.get_json()
  if 'name' not in req_data:
    abort(422)
  name = req_data['name']
  age = req_data['age']
  gender = req_data['gender']

  new_actor = Actor(name=name, age=age, gender=gender)

  db.session.add(new_actor)
  db.session.commit()

  db.session.close()
  return jsonify({
    'success': True
  }), 201

@APP.route('/movies', methods=['GET'])
@requires_auth('get:movies')
def find_movies(token):
  if request.method != 'GET' and request.method != 'POST':
    abort(405)
  try:
    
    movies = Movie.query.order_by('id').all()
    formatted_movies = [movie.format() for movie in movies]

    return jsonify({
      'movies': formatted_movies,
      'success': True
    }), 200

  except Exception:
    abort(422)

@APP.route('/actors', methods=['GET'])
@requires_auth('get:actors')
def find_actors(token):
  if request.method != 'GET' and request.method != 'POST':
    abort(405)
  try:
    
    actors = Actor.query.order_by('id').all()
    formatted_actors = [actor.format() for actor in actors]
    return jsonify({
      'actors': formatted_actors,
      'success': True
    }), 200

  except Exception:
    abort(422)

@APP.route('/movies/<id>', methods=['PATCH'])
@requires_auth('patch:movies')
def update_movie(token, id):

  req_data = request.get_json()
  movie = Movie.query.get(id)

  if not movie:
      abort(404)

  if 'title' in req_data:
      title = req_data['title']
      movie.title = title

  if 'release_date' in req_data:
      release_date = req_data['release_date']
      movie.release_date = release_date

  db.session.commit()

  db.session.close()
  return jsonify({
    'success': True
  }), 200

@APP.route('/actors/<id>', methods=['PATCH'])
@requires_auth('patch:actors')
def update_actor(token, id):

    req_data = request.get_json()
    actor = Actor.query.get(id)

    if not actor:
        abort(404)

    if 'name' in req_data:
        name = req_data['name']
        actor.name = name

    if 'age' in req_data:
        age = req_data['age']
        actor.age = age

    if 'gender' in req_data:
        gender = req_data['gender']
        actor.gender = gender

    db.session.commit()

    db.session.close()
    return jsonify({
      'success': True
    }), 200

@APP.route('/movies/<id>', methods=['DELETE'])
@requires_auth('delete:movies')
def delete_movie(token, id):
    movie = Movie.query.get(id)
    if not movie:
      abort(404)
    db.session.delete(movie)
    db.session.commit()

    return jsonify({
      'success': True
    }), 200

@APP.route('/actors/<id>', methods=['DELETE'])
@requires_auth('delete:actor')
def delete_actor(token, id):
  actor = Actor.query.get(id)
  if not actor:
    abort(404)
  db.session.delete(actor)
  db.session.commit()

  return jsonify({
    'success': True
  }), 200

@APP.errorhandler(404)
def not_found(error):
    return jsonify({
                    "success": False, 
                    "error": 404,
                    "message": "not found"
                    }), 404

@APP.errorhandler(405)
def not_allowed(e):
  return jsonify({
    'success': False,
    'message': 'Not allowed'
  }), 405

@APP.errorhandler(422)
def unprocessable(error):
    return jsonify({
                    "success": False, 
                    "error": 422,
                    "message": "unprocessable"
                    }), 422

if __name__ == '__main__':
    APP.run(host='0.0.0.0', port=8080, debug=True)