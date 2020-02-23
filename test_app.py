import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from app import APP
from models import setup_db, Movie, Actor, db

class CastingTestCase(unittest.TestCase):
    """This class represents the casting test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = APP
        self.client = self.app.test_client
 
        self.database_path = "postgres://postgres:postgres@localhost:5432/casting_test"
        setup_db(self.app, self.database_path)

        self.casting_assistant_auth = {
            'authorization': 'Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IlFVTTRSRVUxUVRWR016VkNPVVV3UXpNd056QTFRek15TlVVeU9USkdRalpCT1RJME9FWkVOUSJ9.eyJpc3MiOiJodHRwczovL3Blbm5jb2ZmZWUuYXV0aDAuY29tLyIsInN1YiI6ImF1dGgwfDVlNGMzODFhZGViYzdkMGVmZjhiZDU4NCIsImF1ZCI6ImNhc3RpbmciLCJpYXQiOjE1ODI0NTg1NzUsImV4cCI6MTU4MjU0MjU3NSwiYXpwIjoiVlF3aWhZbDU5RlE3NzZ1ZVUzbjMxN0Flbnptem11ZzAiLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbImdldDphY3RvcnMiLCJnZXQ6bW92aWVzIl19.QN8Vcef0XTUhHfVQHdCbTQo1ZFGSYhAmxIrYpqAmBf1dkCa6UFZgOq5bbfHyYvLEQy2a0KJiD2HSPOnY7IgffCzepgkwkEuADPZfp7EaDBiqS8D_Y96HE_Z_iBlrP87Sy6LffR925y8rAik0E7M5klz3jsW3f_G9vruV6yxnKFcpWwaaEc_iE5qFoVGxr4WPWRA4vS-By9ZCrHIUCrxyKjSStXV9-kbjj1ZRzsetmIG8lYX7XCishTcdaymqkXXDhtnLwS19JIIKcPwDqjXI90WM6kdticYkgkU8bbBmzMkfGA1GkQLZNjuEzw5nHNlr9nce0nYm61sAVzKK8QgVWQ'
        }

        self.casting_director_auth = {
            'authorization': 'Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IlFVTTRSRVUxUVRWR016VkNPVVV3UXpNd056QTFRek15TlVVeU9USkdRalpCT1RJME9FWkVOUSJ9.eyJpc3MiOiJodHRwczovL3Blbm5jb2ZmZWUuYXV0aDAuY29tLyIsInN1YiI6ImF1dGgwfDVlNGMzN2Y3YmZkZWU2MGYxZjlkYTFkOSIsImF1ZCI6ImNhc3RpbmciLCJpYXQiOjE1ODI0NTg2NDksImV4cCI6MTU4MjU0MjY0OSwiYXpwIjoiVlF3aWhZbDU5RlE3NzZ1ZVUzbjMxN0Flbnptem11ZzAiLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbImRlbGV0ZTphY3RvciIsImdldDphY3RvcnMiLCJnZXQ6bW92aWVzIiwicGF0Y2g6YWN0b3JzIiwicGF0Y2g6bW92aWVzIiwicG9zdDphY3RvcnMiXX0.oRKeq4uS1_lUCg23IgQs2QgYvMNTd_QtGiF4gqHdi8f_Hmmrmm7QfFL19qq2xXerNXxOT75DD60NqQ9o7OT5doix_kesWsJ6edCOUjtGl24ohVGriVOZOLjFHaihEVP_Rx6c6JSi25usZoq8HpRAz6kACyO1-i6UKFrpuknKKYe-gOFFCmtpk3rNTxJx_KUtmyPGjF-KYx9dZzc3mYlMnqjkzP8--9NTQ5l8m5mZfHIgzaOrSh2SRDu2yyKmUNz8QqeNuxvdjM4BXAgIqbKCvXFUYXhRRlU7oE6Tn-U2auIdly9xEnUgI-cKQKoxJUPwshr0wsvPl5R7gKhWtoJdMw'
        }

        self.executive_producer_auth = {
            'authorization': 'Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IlFVTTRSRVUxUVRWR016VkNPVVV3UXpNd056QTFRek15TlVVeU9USkdRalpCT1RJME9FWkVOUSJ9.eyJpc3MiOiJodHRwczovL3Blbm5jb2ZmZWUuYXV0aDAuY29tLyIsInN1YiI6ImF1dGgwfDVlNGMzNzY1MjNiZjNhMGU1YzAwMjI5NiIsImF1ZCI6ImNhc3RpbmciLCJpYXQiOjE1ODI0NTg1MjEsImV4cCI6MTU4MjU0MjUyMSwiYXpwIjoiVlF3aWhZbDU5RlE3NzZ1ZVUzbjMxN0Flbnptem11ZzAiLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbImRlbGV0ZTphY3RvciIsImRlbGV0ZTptb3ZpZXMiLCJnZXQ6YWN0b3JzIiwiZ2V0Om1vdmllcyIsInBhdGNoOmFjdG9ycyIsInBhdGNoOm1vdmllcyIsInBvc3Q6YWN0b3JzIiwicG9zdDptb3ZpZXMiXX0.YTfHmosdQgxk10k5LaErg1Hj60jFzQvSjGQqrqLWKw3sn1aYy7_FWztN4UcTLyH3Qeb0VrGk3T-TpuaZDm_UbO9XLIJLgjBBX2-thwB2cMkrHLkakCfSw4faXTwUKiGFKgXVbKwBdroqt4-A8Xjhuda4RuBOdBDWk5EhMIroRJiXqwcfUcOMPOc0te0KqvkvA99x-RUqhQDZP8pyaMBrMri7nnkkKi4dxsOL77YgSfJeHWIypHJjICxTCv3g73NZxg9u-f921IPsG7MGSGniJl96b1kvl6wB5VSJADAMjdTNMdLmLAzT1s26xhXnEYZXdDAK5rHGNNXYStxaf1q8zw'
        }

        self.starting_movie = {
            'title': 'Babe',
            'release_date': '09-15-98'
        }


        self.new_movie = {
            'title': 'Babe, Pig in the City',
            'release_date': '04-17-00'
        }
        # binds the app to the current context
        with self.app.app_context():
            self.db = db
            self.db.init_app(self.app)
    
            # self.db.drop_all()
            self.db.create_all()

        #Populating test data for delete and patch test. Probably not best practice but will have to do while I learn more about mocking data.
        self.client().post('/movies', json=self.starting_movie, headers=self.executive_producer_auth)     
        self.permissions = [self.casting_assistant_auth, self.casting_director_auth, self.executive_producer_auth]
        self.limited_permissions = [self.casting_assistant_auth, self.casting_director_auth]
    def tearDown(self):
        """Executed after reach test"""
        self.db.drop_all()
        pass


    def test_get_movies(self):
        for permission in self.permissions:
            with self.subTest():
                res = self.client().get('/movies', headers=permission)
                data = json.loads(res.data)

                self.assertEqual(res.status_code, 200)
                self.assertIsNotNone(data['movies'])

    def test_post_movie(self):
        for permission in self.permissions:
            with self.subTest():
                res = self.client().post('/movies', json=self.new_movie, headers=permission)
                #if blocks to check different permissions
                if permission == self.casting_director_auth or permission == self.casting_assistant_auth:
                    self.assertEqual(res.status_code, 401)
                else:
                    self.assertEqual(res.status_code, 201)

    def test_delete_movie_with_perm(self):

        res = self.client().delete('/movies/1', headers=self.executive_producer_auth)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['deleted'], 1)
    
    def test_delete_movie_no_perm(self):
        for permission in self.limited_permissions:
            with self.subTest():
                res = self.client().delete('/movies/1', headers=permission)
                
                self.assertEqual(res.status_code, 401)



    # def test_delete_movie(self):
    #     res = self.client().delete('/movies/4', headers=self.executive_producer_auth)
    #     data = json.loads(res.data)

    #     self.assertEqual(res.status_code, 200)
    #     self.assertEqual(data['delete'], 4)
# class DupCastingTestCase(unittest.TestCase):
#     """This class represents the casting test case"""

#     def setUp(self):
#         """Define test variables and initialize app."""
#         self.app = APP
#         self.client = self.app.test_client
 
#         self.database_path = "postgres://postgres:postgres@localhost:5432/casting_test"
#         setup_db(self.app, self.database_path)

#         # binds the app to the current context
#         with self.app.app_context():
#             self.db = db
#             self.db.init_app(self.app)
#             # create all tables
#             self.db.create_all()


#         self.casting_assistant_auth = {
#             'authorization': 'Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IlFVTTRSRVUxUVRWR016VkNPVVV3UXpNd056QTFRek15TlVVeU9USkdRalpCT1RJME9FWkVOUSJ9.eyJpc3MiOiJodHRwczovL3Blbm5jb2ZmZWUuYXV0aDAuY29tLyIsInN1YiI6ImF1dGgwfDVlNGMzODFhZGViYzdkMGVmZjhiZDU4NCIsImF1ZCI6ImNhc3RpbmciLCJpYXQiOjE1ODI0NTg1NzUsImV4cCI6MTU4MjU0MjU3NSwiYXpwIjoiVlF3aWhZbDU5RlE3NzZ1ZVUzbjMxN0Flbnptem11ZzAiLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbImdldDphY3RvcnMiLCJnZXQ6bW92aWVzIl19.QN8Vcef0XTUhHfVQHdCbTQo1ZFGSYhAmxIrYpqAmBf1dkCa6UFZgOq5bbfHyYvLEQy2a0KJiD2HSPOnY7IgffCzepgkwkEuADPZfp7EaDBiqS8D_Y96HE_Z_iBlrP87Sy6LffR925y8rAik0E7M5klz3jsW3f_G9vruV6yxnKFcpWwaaEc_iE5qFoVGxr4WPWRA4vS-By9ZCrHIUCrxyKjSStXV9-kbjj1ZRzsetmIG8lYX7XCishTcdaymqkXXDhtnLwS19JIIKcPwDqjXI90WM6kdticYkgkU8bbBmzMkfGA1GkQLZNjuEzw5nHNlr9nce0nYm61sAVzKK8QgVWQ'
#         }

#         self.casting_director_auth = {
#             'authorization': 'Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IlFVTTRSRVUxUVRWR016VkNPVVV3UXpNd056QTFRek15TlVVeU9USkdRalpCT1RJME9FWkVOUSJ9.eyJpc3MiOiJodHRwczovL3Blbm5jb2ZmZWUuYXV0aDAuY29tLyIsInN1YiI6ImF1dGgwfDVlNGMzN2Y3YmZkZWU2MGYxZjlkYTFkOSIsImF1ZCI6ImNhc3RpbmciLCJpYXQiOjE1ODI0NTg2NDksImV4cCI6MTU4MjU0MjY0OSwiYXpwIjoiVlF3aWhZbDU5RlE3NzZ1ZVUzbjMxN0Flbnptem11ZzAiLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbImRlbGV0ZTphY3RvciIsImdldDphY3RvcnMiLCJnZXQ6bW92aWVzIiwicGF0Y2g6YWN0b3JzIiwicGF0Y2g6bW92aWVzIiwicG9zdDphY3RvcnMiXX0.oRKeq4uS1_lUCg23IgQs2QgYvMNTd_QtGiF4gqHdi8f_Hmmrmm7QfFL19qq2xXerNXxOT75DD60NqQ9o7OT5doix_kesWsJ6edCOUjtGl24ohVGriVOZOLjFHaihEVP_Rx6c6JSi25usZoq8HpRAz6kACyO1-i6UKFrpuknKKYe-gOFFCmtpk3rNTxJx_KUtmyPGjF-KYx9dZzc3mYlMnqjkzP8--9NTQ5l8m5mZfHIgzaOrSh2SRDu2yyKmUNz8QqeNuxvdjM4BXAgIqbKCvXFUYXhRRlU7oE6Tn-U2auIdly9xEnUgI-cKQKoxJUPwshr0wsvPl5R7gKhWtoJdMw'
#         }

#         self.executive_producer_auth = {
#             'authorization': 'Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IlFVTTRSRVUxUVRWR016VkNPVVV3UXpNd056QTFRek15TlVVeU9USkdRalpCT1RJME9FWkVOUSJ9.eyJpc3MiOiJodHRwczovL3Blbm5jb2ZmZWUuYXV0aDAuY29tLyIsInN1YiI6ImF1dGgwfDVlNGMzNzY1MjNiZjNhMGU1YzAwMjI5NiIsImF1ZCI6ImNhc3RpbmciLCJpYXQiOjE1ODI0NTg1MjEsImV4cCI6MTU4MjU0MjUyMSwiYXpwIjoiVlF3aWhZbDU5RlE3NzZ1ZVUzbjMxN0Flbnptem11ZzAiLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbImRlbGV0ZTphY3RvciIsImRlbGV0ZTptb3ZpZXMiLCJnZXQ6YWN0b3JzIiwiZ2V0Om1vdmllcyIsInBhdGNoOmFjdG9ycyIsInBhdGNoOm1vdmllcyIsInBvc3Q6YWN0b3JzIiwicG9zdDptb3ZpZXMiXX0.YTfHmosdQgxk10k5LaErg1Hj60jFzQvSjGQqrqLWKw3sn1aYy7_FWztN4UcTLyH3Qeb0VrGk3T-TpuaZDm_UbO9XLIJLgjBBX2-thwB2cMkrHLkakCfSw4faXTwUKiGFKgXVbKwBdroqt4-A8Xjhuda4RuBOdBDWk5EhMIroRJiXqwcfUcOMPOc0te0KqvkvA99x-RUqhQDZP8pyaMBrMri7nnkkKi4dxsOL77YgSfJeHWIypHJjICxTCv3g73NZxg9u-f921IPsG7MGSGniJl96b1kvl6wB5VSJADAMjdTNMdLmLAzT1s26xhXnEYZXdDAK5rHGNNXYStxaf1q8zw'
#         }

#         self.new_movie = {
#             'title': 'Jackass',
#             'release_date': '04-17-00'
#         }
        
#         self.permissions = [self.executive_producer_auth, self.casting_assistant_auth, self.casting_director_auth]

#     def tearDown(self):
#         """Executed after reach test"""
#         pass


#     def test_get_movies(self):
#         for permission in self.permissions:
#             with self.subTest():
#                 res = self.client().get('/movies', headers=permission)
#                 data = json.loads(res.data)

#                 self.assertEqual(res.status_code, 200)
#                 self.assertIsNotNone(data['movies'])

if __name__ == "__main__":
    unittest.main()