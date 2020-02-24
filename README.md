A casting agency app that lists movies and actors.

Run pip install -r requirements.txt to install the dependencies
Set the variable FLASK_APP=app.py
Run the command "flask run" to start

To run the test suite, run "python test_app.py"

##ROUTES
#At this stage the responses from the API are minimal, until the requirements for
#the frontend are determined.


GET '/movies'
-Returns a list of all movies in the database

GET '/actors'
-Returns a list of all actors in the database

POST '/movies'
-Takes a dictionary object in the request body with the following format and creates a new movie:
{
    'title': String,
    'release_date': String
}

POST '/actors'
-Takes a dictionary object in the request body with the following format and creates a new actor:
{
    'name': String,
    'age': Integer,
    'gender': String
}

PATCH '/movies/<id>'
-Takes an id from the request URL and finds the corresponding movie to update with the provided information in the request body

PATCH '/actors/<id>'
-Takes an id from the request URL and finds the corresponding actor to update with the provided information in the request body

DELETE '/movies/<id>'
-Takes an id from the request URL and finds the corresponding movie to delete

DELETE '/actors/<id>'
-Takes an id from the request URL and finds the corresponding actor to delete