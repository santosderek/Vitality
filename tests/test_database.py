import unittest
from flask import Flask
from flask_pymongo import PyMongo
from vitality.database import Database
from vitality.user import User
from vitality.workout import Workout
from vitality.configuration import Configuration

app = Flask(__name__)
config = Configuration()
app.config["MONGO_URI"] = config.get_local_uri()
mongo = PyMongo(app)


class TestDatabase(unittest.TestCase):

    def test_add_user(self):

        # Creating database object
        database = Database(app)

        # Creating new User object
        new_user = User(
            None,
            username="test",
            password="password",
            firstname="first",
            lastname="last",
            location="Earth",
            phone=1234567890)

        # Remove test user
        while database.get_user_class_by_username(new_user.username):
            db_user = database.get_user_class_by_username(new_user.username)
            database.remove_user(db_user.id)

        # Adding new user
        database.add_user(new_user)

        # Geting the new user by their username
        db_user = database.get_user_class_by_username(new_user.username)

        # Setting our current user object's id as mongodb id
        new_user.id = db_user.id

        self.assertTrue (db_user.as_dict() == new_user.as_dict())

        # Removing temp user from database
        database.remove_user(db_user.id)
        self.assertTrue(database.get_by_id(db_user.id) == None)

    def test_add_workout(self):
        # Creating database object
        database = Database(app)

        # Creating new User object
        new_user = User(
            None,
            username="test",
            password="password",
            firstname="first",
            lastname="last",
            location="Mars",
            phone=9876543210)

        # Remove test user
        while database.get_user_class_by_username(new_user.username):
            db_user = database.get_user_class_by_username(new_user.username)
            database.remove_user(db_user.id)

        # Adding new user
        database.add_user(new_user)

        db_user = database.get_user_class_by_username(new_user.username)
        # Creating a new Workout object
        new_workout = Workout(
            None,
            creator_id = new_user.id,
            name="testing",
            difficulty="easy",
            about="workout",
            exp_rewards=10)

        database.add_workout(new_workout)
        # Getting the new user by their username

        # Getting the workout by their name
        db_workout = database.get_workout_class_by_name(new_workout.name)

        # Sets the id
        new_workout.id = db_workout.id

        #sets creator's id
        new_workout.creator_id = db_user.id
        db_workout.creator_id = new_workout.creator_id
        self.assertTrue(db_user.id == new_workout.creator_id)
        self.assertTrue(db_workout.as_dict() == new_workout.as_dict())
        # Removing temp workout from database
        database.remove_workout(new_workout.id)
        self.assertTrue(database.get_workout_class_by_id(db_workout.id) == None)

        # Removing temp user from database
        database.remove_user(db_user.id)
        self.assertTrue(database.get_by_id(db_user.id) == None)

    def test_set_username(self):

        # Creating database object
        database = Database(app)

        # Creating new User object
        new_user = User(
            None,
            username="test",
            password="password",
            firstname="first",
            lastname="last",
            location="Earth",
            phone=1234567890)

        # Remove test user
        while database.get_user_class_by_username(new_user.username):
            db_user = database.get_user_class_by_username(new_user.username)
            database.remove_user(db_user.id)

        # Adding new user
        database.add_user(new_user)

        # Geting the new user by their username
        db_user_1 = database.get_user_class_by_username(new_user.username)

        # Setting our current user object's id as mongodb id
        new_user.id = db_user_1.id

        # Checking if user objects are the same through their dicts
        self.assertTrue (db_user_1.as_dict() == new_user.as_dict())

        # Changing new user's name to 'elijah'
        new_user.username = "elijah"
        database.set_username(new_user.id, new_user.username)

        # Checking if database updated
        db_user_2 = database.get_user_class_by_id(new_user.id)

        self.assertTrue (db_user_2.as_dict() == new_user.as_dict())

        # Removing temp user from database
        database.remove_user(db_user_2.id)
        self.assertTrue(database.get_by_id(db_user_2.id) == None)

    def test_set_password(self):

        # Creating database object
        database = Database(app)

        # Creating new User object
        new_user = User(
            None,
            username="test",
            password="password",
            firstname="first",
            lastname="last",
            location="Earth",
            phone=1234567890)

        # Remove test user
        while database.get_user_class_by_username(new_user.username):
            db_user = database.get_user_class_by_username(new_user.username)
            database.remove_user(db_user.id)

        # Adding new user
        database.add_user(new_user)

        # Updating user object to database user
        new_user = database.get_user_class_by_username(new_user.username)

        # Changing password
        new_user.password = "newPassword"
        database.set_password(new_user.id, new_user.password)

        # Checking password
        db_user = database.get_user_class_by_username(new_user.username)
        self.assertTrue(db_user.password == new_user.password)

        database.remove_user(db_user.id)
        self.assertTrue(database.get_user_class_by_id(db_user.id) == None)

    def test_set_location(self):

        # Creating database object
        database = Database(app)

        # Creating new User object
        new_user = User(
            None,
            username="test",
            password="password",
            firstname="first",
            lastname="last",
            location="Earth",
            phone=1234567890)

        # Remove test user
        while database.get_user_class_by_username(new_user.username):
            db_user = database.get_user_class_by_username(new_user.username)
            database.remove_user(db_user.id)

        # Adding new user
        database.add_user(new_user)

        # Updating user object to database user
        new_user = database.get_user_class_by_username(new_user.username)

        # Changing location
        new_user.location = "newLocation"
        database.set_location(new_user.id, new_user.location)

        # Checking location
        db_user = database.get_user_class_by_username(new_user.username)
        self.assertTrue(db_user.location == new_user.location)

        database.remove_user(db_user.id)
        self.assertTrue(database.get_user_class_by_id(db_user.id) == None)

        def test_set_phone(self):

            # Creating database object
            database = Database(app)

            # Creating new User object
            new_user = User(
                None,
                username="test",
                password="password",
                firstname="first",
                lastname="last",
                location="Earth",
                phone=1234567890)

            # Remove test user
            while database.get_user_class_by_username(new_user.username):
                db_user = database.get_user_class_by_username(new_user.username)
                database.remove_user(db_user.id)

            # Adding new user
            database.add_user(new_user)

            # Updating user object to database user
            new_user = database.get_user_class_by_username(new_user.username)

            # Changing phone
            new_user.phone = "newPhone"
            database.set_phone(new_user.id, new_user.phone)

            # Checking phone
            db_user = database.get_user_class_by_username(new_user.username)
            self.assertTrue(db_user.phone == new_user.phone)

            database.remove_user(db_user.id)
            self.assertTrue(database.get_user_class_by_id(db_user.id) == None)

    def test_set_firstname(self):

        # Creating database object
        database = Database(app)

        # Creating new User object
        new_user = User(
            None,
            username="test",
            password="password",
            firstname="first",
            lastname="last",
            location="Earth",
            phone=1234567890)

        # Remove test user
        while database.get_user_class_by_username(new_user.username):
            db_user = database.get_user_class_by_username(new_user.username)
            database.remove_user(db_user.id)

        # Adding new user
        database.add_user(new_user)

        # Updating user object to database user
        new_user = database.get_user_class_by_username(new_user.username)

        # Changing firstname
        new_user.firstname = "newfirstname"
        database.set_firstname(new_user.id, new_user.firstname)

        # Checking firstname
        db_user = database.get_user_class_by_username(new_user.username)
        self.assertTrue(db_user.firstname == new_user.firstname)

        database.remove_user(db_user.id)
        self.assertTrue(database.get_user_class_by_username(db_user.id) == None)

    def test_set_lastname(self):

        # Creating database object
        database = Database(app)

        # Creating new User object
        new_user = User(
            None,
            username="test",
            password="password",
            firstname="first",
            lastname="last",
            location="Earth",
            phone=1234567890)

        # Remove test user
        while database.get_user_class_by_username(new_user.username):
            db_user = database.get_user_class_by_username(new_user.username)
            database.remove_user(db_user.id)

        # Adding new user
        database.add_user(new_user)

        # Updating user object to database user
        new_user = database.get_user_class_by_username(new_user.username)

        # Changing lastname
        new_user.lastname = "newlastname"
        database.set_lastname(new_user.id, new_user.lastname)

        # Checking lastname
        db_user = database.get_user_class_by_username(new_user.username)
        self.assertTrue(db_user.lastname == new_user.lastname)

        database.remove_user(db_user.id)
        self.assertTrue(database.get_user_class_by_id(db_user.id) == None)

if __name__ == '__main__':
    unittest.main()
