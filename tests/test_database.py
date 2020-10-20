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
        new_user = User(
            None, 
            username="derek", 
            password="derek",
            firstname="derek",
            lastname="santos",
            location="Earth",
            phone=1234567890)

        # Adding new user
        database.add_user(new_user)

        # Geting the new user by their username 
        db_get = database.get_user_class_by_username(new_user.username)

        # Setting our current user object's id as mongodb id
        new_user.id = db_get.id

        # Checking if user objects are the same through their dicts
        
        self.assertTrue (db_get.as_dict() == new_user.as_dict())

        # Changing new user's name to 'elijah'
        new_user.username = "elijah"
        database.set_username(new_user.id, new_user.username)

        # Checking if database updated
        db_get_2 = database.get_user_class_by_username(new_user.username)

        self.assertTrue (db_get_2.as_dict() == new_user.as_dict())

        # Removing temp user from database
        database.remove_user(db_get_2.id)
        self.assertTrue(database.get_by_id(db_get_2.id) == None)


if __name__ == '__main__':
    unittest.main()