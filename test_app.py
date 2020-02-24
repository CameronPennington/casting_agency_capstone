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
            'authorization': 'Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IlFVTTRSRVUxUVRWR016VkNPVVV3UXpNd056QTFRek15TlVVeU9USkdRalpCT1RJME9FWkVOUSJ9.eyJpc3MiOiJodHRwczovL3Blbm5jb2ZmZWUuYXV0aDAuY29tLyIsInN1YiI6ImF1dGgwfDVlNGMzODFhZGViYzdkMGVmZjhiZDU4NCIsImF1ZCI6ImNhc3RpbmciLCJpYXQiOjE1ODI1NDc5MDcsImV4cCI6MTU4MjYzMTkwNywiYXpwIjoiVlF3aWhZbDU5RlE3NzZ1ZVUzbjMxN0Flbnptem11ZzAiLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbImdldDphY3RvcnMiLCJnZXQ6bW92aWVzIl19.VIlYXwKLITmhcoPH8Y7SiSK-dtuq-KH82Cy7eVatr0VacTjn9fX4WmHw28337Fs8PJjmSvSp2lxRRKgi54rNlXUC6rQJuPmFybSPIPOreLLmfTg_jcQzR1TSAXkIcX_33liqN5xKf-AykbPo66Z2qeWNSEstpuZwavzkKlsDkULylVZ6Ir4S06DD9pHa11p86M4Xv-EHlFYq4u6uz_Pj_huSOuG4N5kOCcC2X5SrRGgusNlbjJaiMTJtyToByGaiSOONr13zN1zWfH3Dg5rnqdjJ-YOq79es7xF8LcGBA1IkiY1YheF3ZKM-doqkTFj5ofOEIaKUJKtOHCNza3rwVw'
        }

        self.casting_director_auth = {
            'authorization': 'Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IlFVTTRSRVUxUVRWR016VkNPVVV3UXpNd056QTFRek15TlVVeU9USkdRalpCT1RJME9FWkVOUSJ9.eyJpc3MiOiJodHRwczovL3Blbm5jb2ZmZWUuYXV0aDAuY29tLyIsInN1YiI6ImF1dGgwfDVlNGMzN2Y3YmZkZWU2MGYxZjlkYTFkOSIsImF1ZCI6ImNhc3RpbmciLCJpYXQiOjE1ODI1NDc4MzcsImV4cCI6MTU4MjYzMTgzNywiYXpwIjoiVlF3aWhZbDU5RlE3NzZ1ZVUzbjMxN0Flbnptem11ZzAiLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbImRlbGV0ZTphY3RvciIsImdldDphY3RvcnMiLCJnZXQ6bW92aWVzIiwicGF0Y2g6YWN0b3JzIiwicGF0Y2g6bW92aWVzIiwicG9zdDphY3RvcnMiXX0.vHf-PVGLO6cVvTPYcGvp4ADNXrTj2PFqR_j_CzXRLcoMGEPjiTMvru6Sf7ZEtqbOThyHZC_CIH2rV7vb957ktqVCcDP6NnqALCofjWXMuFEHFw4KZEqBs3hiFc_Ipy4SFmFtG3vg44xq8yR1IzqeG6HhP3_uVZ2otRQ7UwBfM0Yrx3tLVeKU-Rzrp7Wz4vD4ywdF80z1uOZhtFV46TmKiO0F0O0ffErcjRusiF1olva9mbbEDGqFJ8QrMyi7QgOaR2CrQ1A_h3qKp_5lfGbs7a8hjOvGvxuARmZoB7k4uXtIrM6VJcYP815xQ6mWT7dI1jwV70wZ_1JHVRWVRIeeGg'
        }

        self.executive_producer_auth = {
            'authorization': 'Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IlFVTTRSRVUxUVRWR016VkNPVVV3UXpNd056QTFRek15TlVVeU9USkdRalpCT1RJME9FWkVOUSJ9.eyJpc3MiOiJodHRwczovL3Blbm5jb2ZmZWUuYXV0aDAuY29tLyIsInN1YiI6ImF1dGgwfDVlNGMzNzY1MjNiZjNhMGU1YzAwMjI5NiIsImF1ZCI6ImNhc3RpbmciLCJpYXQiOjE1ODI1NDc3ODUsImV4cCI6MTU4MjYzMTc4NSwiYXpwIjoiVlF3aWhZbDU5RlE3NzZ1ZVUzbjMxN0Flbnptem11ZzAiLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbImRlbGV0ZTphY3RvciIsImRlbGV0ZTptb3ZpZXMiLCJnZXQ6YWN0b3JzIiwiZ2V0Om1vdmllcyIsInBhdGNoOmFjdG9ycyIsInBhdGNoOm1vdmllcyIsInBvc3Q6YWN0b3JzIiwicG9zdDptb3ZpZXMiXX0.ThfwoC0WGULun2lKZXBkJ96tMcn7i3WH1hROQpQWLH0W4W74CdXdMkNhVpDYFtutnDd2f5OR3t-34H1POSnnI7LAPjnx_tkOMzS7VZgL03aXkCB-tGLGjMQRjL0CJkjwxZON-RVyKwUxiGMjlgpRTtXXFrULZ-Z05tp5_pf8I_ezU2bD_AYLaBLnpiZluTab2OydEsfm1XjKC2nx84TEoYz7z9BrPZjc3NrkFhUQeFiJbSpPAb2M3F7Fv8Kqt5LXEzytVgvCL3WsseBSM-wPLpCis9amdzKPGV4gywLm-rCUvSVawQqzEDy-tsCnuegKuww2BqPMBOQUfDXbCrJpkQ'
        }

        self.starting_movie = {
            'title': 'Babe',
            'release_date': '09-15-98'
        }

        self.new_movie = {
            'title': 'Babe, Pig in the City',
            'release_date': '04-17-00'
        }

        self.patch_movie = {
            'title': 'Godzilla'
        }

        self.starting_actor = {
            'name': 'Jonathan Lipnicki',
            'age': '28',
            'gender': 'male'
        }

        self.new_actor = {
            'name': 'Taraji P. Henson',
            'age': '40',
            'gender': 'female'
        }

        self.new_actor_2 = {
            'name': 'Bernard',
            'age': '40',
            'gender': 'non-binary'
        }

        self.patch_actor = {
            'age': '29'
        }

        # binds the app to the current context
        with self.app.app_context():
            self.db = db
            self.db.init_app(self.app)
    
            # self.db.drop_all()
            self.db.create_all()

        #Populating test data for delete and patch test. Probably not best practice but will have to do while I learn more about mocking data.
        self.client().post('/movies', json=self.starting_movie, headers=self.executive_producer_auth)
        self.client().post('/actors', json=self.starting_actor, headers=self.executive_producer_auth)  
        #Different combinations of permissions for testing      
        self.permissions = [self.casting_assistant_auth, self.casting_director_auth, self.executive_producer_auth]
        self.limited_permissions = [self.casting_assistant_auth, self.casting_director_auth]
        self.elevated_permissions = [self.casting_director_auth, self.executive_producer_auth]

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

    def test_patch_movie(self):
        for permission in self.permissions:
            with self.subTest():
                res = self.client().patch('/movies/1', json=self.patch_movie, headers=permission)
                #if blocks to check different permissions
                if permission == self.casting_assistant_auth:
                    self.assertEqual(res.status_code, 401)
                else:
                    self.assertEqual(res.status_code, 200)

    def test_delete_movie_with_perm(self):

        res = self.client().delete('/movies/1', headers=self.executive_producer_auth)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
    
    def test_delete_movie_no_perm(self):
        for permission in self.limited_permissions:
            with self.subTest():
                res = self.client().delete('/movies/1', headers=permission)
                
                self.assertEqual(res.status_code, 401)

    def test_get_actors(self):
        for permission in self.permissions:
            with self.subTest():
                res = self.client().get('/actors', headers=permission)
                data = json.loads(res.data)

                self.assertEqual(res.status_code, 200)
                self.assertIsNotNone(data['actors'])
#need to break into different tests
    def test_post_actor_casting_assistant(self):
        res = self.client().post('/actors', json=self.new_actor, headers=self.casting_assistant_auth)
        
        self.assertEqual(res.status_code, 401)

    def test_post_actor_casting_director(self):
        res = self.client().post('/actors', json=self.new_actor, headers=self.casting_director_auth)
        
        self.assertEqual(res.status_code, 201)

    def test_post_actor_executive_producer(self):
        res = self.client().post('/actors', json=self.new_actor, headers=self.executive_producer_auth)
        
        self.assertEqual(res.status_code, 201)

    def test_patch_actor(self):
        for permission in self.permissions:
            with self.subTest():
                res = self.client().patch('/actors/1', json=self.patch_actor, headers=permission)
                #if blocks to check different permissions
                if permission == self.casting_assistant_auth:
                    self.assertEqual(res.status_code, 401)
                else:
                    self.assertEqual(res.status_code, 200)

    def test_delete_actor_casting_assistant(self):
        res = self.client().delete('/actors/1', headers=self.casting_assistant_auth)

        self.assertEqual(res.status_code, 401)

    def test_delete_actor_casting_director(self):
        res = self.client().delete('/actors/1', headers=self.casting_director_auth)

        self.assertEqual(res.status_code, 200)
    
    def test_delete_actor_executive_producer(self):
        res = self.client().delete('/actors/1', headers=self.executive_producer_auth)

        self.assertEqual(res.status_code, 200)

    def test_delete_movie_404(self):
        res = self.client().delete('/movies/1000', headers=self.executive_producer_auth)

        self.assertEqual(res.status_code, 404)

    def test_delete_actor_404(self):
        res = self.client().delete('/actors/1000', headers=self.executive_producer_auth)

        self.assertEqual(res.status_code, 404)

    def test_get_actors_405(self):
        res = self.client().delete('/actors', headers=self.executive_producer_auth)

        self.assertEqual(res.status_code, 405)

    def test_get_movies_405(self):
        res = self.client().delete('/movies', headers=self.executive_producer_auth)

        self.assertEqual(res.status_code, 405)

    def test_patch_movies_404(self):
        res = self.client().patch('/movies/1000', headers=self.executive_producer_auth)

        self.assertEqual(res.status_code, 404)

    def test_patch_actors_404(self):
        res = self.client().patch('/actors/1000', headers=self.executive_producer_auth)

        self.assertEqual(res.status_code, 404)

    def test_post_actors_422(self):
        res = self.client().post('/actors', json={}, headers=self.executive_producer_auth)

        self.assertEqual(res.status_code, 422)

    def test_post_movies_422(self):
        res = self.client().post('/movies', json={}, headers=self.executive_producer_auth)

        self.assertEqual(res.status_code, 422)

if __name__ == "__main__":
    unittest.main()