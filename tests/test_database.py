import unittest
from flask import Flask
from flask_pymongo import PyMongo
from vitality.database import Database
from vitality.user import User


app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb://localhost:27017/flaskDatabase"
mongo = PyMongo(app)

class TestDatabase(unittest.TestCase):
    def test_set_username(self):
        # Creating database object
        database = Database(app)

        # Creating new User object
        new_user = User(-99.0, username="derek", password="derek")
        
        # Adding new user
        database.add_user(new_user)

        # Geting the new user by their username 
        db_get = database.get_by_username(new_user.username)
        db_get.pop('_id')
        self.assertTrue (db_get == new_user.as_dict())

        # Changing new user's name to 'elijah'
        new_user.username = "elijah"
        database.set_username(new_user.id, new_user.username)

        # Checking if database updated
        db_get_2 = database.get_by_username(new_user.username)
        db_get_2.pop('_id')
        self.assertTrue (db_get_2 == new_user.as_dict())

        # Removing temp user from database
        database.remove_user(1)
        self.assertTrue(database.get_by_id(1) == None)


if __name__ == '__main__':
    unittest.main()