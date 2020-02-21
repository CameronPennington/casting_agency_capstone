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

        # binds the app to the current context
        with self.app.app_context():
            self.db = db
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()


        self.casting_assistant_auth = {
            'authorization': 'Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IlFVTTRSRVUxUVRWR016VkNPVVV3UXpNd056QTFRek15TlVVeU9USkdRalpCT1RJME9FWkVOUSJ9.eyJpc3MiOiJodHRwczovL3Blbm5jb2ZmZWUuYXV0aDAuY29tLyIsInN1YiI6ImF1dGgwfDVlNGMzODFhZGViYzdkMGVmZjhiZDU4NCIsImF1ZCI6ImNhc3RpbmciLCJpYXQiOjE1ODIzMDA2NzIsImV4cCI6MTU4MjM4NDY3MiwiYXpwIjoiVlF3aWhZbDU5RlE3NzZ1ZVUzbjMxN0Flbnptem11ZzAiLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbImdldDphY3RvcnMiLCJnZXQ6bW92aWVzIl19.PYkzWkL-X4fEjnYFOSZKFVAU4XIAtyRz7o1Ibix-IuGU1AvYYdN2hib82qSR0HSwJTBnR_6ldH-tmMN2EVZGwcxNJyZfyBBbbyTvtpBED2P8rtwjPdtXzx99D_xsYZr0zxNjhbqe2QVe0GcpNfqnWqBHV5O0bZoF69KiP5W3_C_QQm70MpphikbrapCXipUZJQS5HkOH7IBepDNQDzpbavWXr7n-mRL04v0l2wcf8S0dnZXM-hd_bEY3uvcfBRfbf5j00OTzv5mLsP3ZhdzILuxC9arJ8KBMWMGOITlbOzot5NNnPXkNdi7YkZcKpI71EwPwpIU8C4jRfAdCpr1xig'
        }

        self.casting_director_auth = {
            'authorization': 'Bearer '
        }

        self.executive_producer_auth = {
            'authorization': 'Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IlFVTTRSRVUxUVRWR016VkNPVVV3UXpNd056QTFRek15TlVVeU9USkdRalpCT1RJME9FWkVOUSJ9.eyJpc3MiOiJodHRwczovL3Blbm5jb2ZmZWUuYXV0aDAuY29tLyIsInN1YiI6ImF1dGgwfDVlNGMzNzY1MjNiZjNhMGU1YzAwMjI5NiIsImF1ZCI6ImNhc3RpbmciLCJpYXQiOjE1ODIzMDI2MTQsImV4cCI6MTU4MjM4NjYxNCwiYXpwIjoiVlF3aWhZbDU5RlE3NzZ1ZVUzbjMxN0Flbnptem11ZzAiLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbImRlbGV0ZTphY3RvciIsImRlbGV0ZTptb3ZpZXMiLCJnZXQ6YWN0b3JzIiwiZ2V0Om1vdmllcyIsInBhdGNoOmFjdG9ycyIsInBhdGNoOm1vdmllcyIsInBvc3Q6YWN0b3JzIiwicG9zdDptb3ZpZXMiXX0.mMPRE2KUR0nJ3Tr8RBEbKg9ro6g3_k4Vg0yIevvmDSl3DRzD5onRaxUxMAgPhznqYI7mHOqV2I4epDo_o5nuw30QF53E_OXDtKUF60eWD7yjF8bC1SYSlEPHb5sbcGf9zEr5wqZdM9bMzxnbCpYH2O0aqrBaFQy31Ud5jI6h-9EQg-I2CpaH5qP0aeLFZ6ZhSHQr141Qo5gnZ75FP-edAAwNq4fplExNE6t8ViDlGOXuxEFnHyay4sILo43o78QoQQiqOrmPsw_vPNWJphEs7ps8JJ0_tF7kmAmR4XHYle5J8Nh3cNlyEuAdum2zTZHUbV775Y8SHxQs9vOhpejqRA'
        }

        self.new_movie = {
            'title': 'Jackass',
            'release_date': '04-17-00'
        }
        

    def tearDown(self):
        """Executed after reach test"""
        pass

    def test_get_movies(self):
        res = self.client().get('/movies', headers=self.casting_assistant_auth)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertIsNotNone(data['movies'])

    def test_create_movie(self):
        res = self.client().post('/movies', json=self.new_movie, headers=self.executive_producer_auth)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 201)

    def test_delete_movie(self):
        res = self.client().delete('/movies/4', headers=self.executive_producer_auth)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['delete'], 4)

if __name__ == "__main__":
    unittest.main()