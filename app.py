import os
from flask import Flask, request, abort, jsonify
from sqlalchemy import exc
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from models import setup_db, Movie, Actor
from auth import requires_auth

def create_app(test_config=None):
  # create and configure the app
  app = Flask(__name__)
  setup_db(app)
  db = SQLAlchemy()
  CORS(app)

  return app

APP = create_app()

@APP.route('/movies', methods=['POST'])
@requires_auth('post:movies')
def create_movie(token):
  try:
    if request.method != 'GET' and request.method != 'POST':
      abort(405)
    
    req_data = request.get_json()
    print(req_data)
    new_movie = Movie(
      title = req_data['title'],
      release_date = req_data['release_date']
    )

    db.session.add(new_movie)
    db.session.commit()
  except Exception:
    db.session.rollback()
    abort(422)
  finally:
    db.session.close()
    return jsonify({
      'success': True
    })

if __name__ == '__main__':
    APP.run(host='0.0.0.0', port=8080, debug=True)