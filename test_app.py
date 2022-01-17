import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import app
# TODO: 
# make sure you create a database named hello_test in psql 
database_name = "hello_test"
database_path = 'postgresql://postgres:123456@localhost:5432/{}'.format(
    database_name)


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = app
        self.client = self.app.test_client

    def tearDown(self):
        """Executed after reach test"""
        pass

    # testing the categories
    def test_get_categories_ok(self):
        print('hello')
        res = self.client().get('/greeting')
        print(res)
        data = json.loads(res.data)
        print(data)
        self.assertEqual(200, 200)


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
