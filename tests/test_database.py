import unittest
from copy import deepcopy
from flask import Flask
from flask_pymongo import PyMongo
from vitality import create_app
from vitality.database import (
    Database,
    WorkoutCreatorIdNotFound,
    UsernameTakenError,
    password_sha256
)
from vitality.trainee import Trainee
from vitality.trainer import Trainer
from vitality.workout import Workout
from vitality.configuration import Configuration


class TestDatabase(unittest.TestCase):
    # Creating database object
    database = Database(create_app())

    # Creating new Trainee object
    test_trainee = Trainee(
        _id=None,
        username="testTrainee",
        password="password",
        name="first last",
        location="Earth",
        phone=1234567890,
        trainers=[])

    # Creating new Trainer object
    test_trainer = Trainer(
        _id=None,
        username="testTrainer",
        password="password",
        name="first last",
        location="mars",
        phone=1234567890,
        trainees=[])

    # Creating new Workout Object
    test_workout = Workout(
        _id=None,
        creator_id=None,
        name="testing",
        difficulty="easy",
        about="workout",
        exp=10)

    def setUp(self):
        self.tearDown()
        self.assertTrue(self.test_trainee.password == 'password')
        self.database.add_trainee(self.test_trainee)
        self.database.add_trainer(self.test_trainer)

        # Add workout
        self.test_workout.creator_id = self.database.get_trainee_by_username(
            self.test_trainee.username)._id
        self.database.add_workout(self.test_workout)

        self.assertTrue(self.test_trainee.password == 'password')

    def tearDown(self):
        # Remove test Trainee if found
        while self.database.get_trainee_by_username(self.test_trainee.username) is not None:
            db_user = self.database.get_trainee_by_username(
                self.test_trainee.username)
            self.database.remove_trainee(db_user._id)

        # Remove test Trainer if found
        while self.database.get_trainer_by_username(self.test_trainer.username) is not None:
            db_user = self.database.get_trainer_by_username(
                self.test_trainer.username)
            self.database.remove_trainer(db_user._id)

        # Remove test Workout if found
        while self.database.get_workout_class_by_name(self.test_workout.name) is not None:
            db_user = self.database.get_workout_class_by_name(
                self.test_workout.name)
            self.database.remove_workout(db_user._id)

    def test_password_sha256(self):
        password = 'asupersecretpassword'
        hashed_password = '009e3e71eed006baa4441cdc417e58f72a635e52f814400e6301881620628d8b'
        self.assertTrue(password_sha256(password) == hashed_password)

    """Trainee tests"""

    def test_add_trainee(self):

        # Raise exception if 'testTrainee' username found
        with self.assertRaises(UsernameTakenError):
            new_trainer = deepcopy(self.test_trainer)
            new_trainer.username = "testTrainee"
            self.database.add_trainee(new_trainer)

        # Raise exception if 'testTrainer' username found
        with self.assertRaises(UsernameTakenError):
            new_trainer = deepcopy(self.test_trainer)
            new_trainer.username = "testTrainer"
            self.database.add_trainee(new_trainer)

        # Copy test_trainer and change to unused trainer name
        new_trainee = deepcopy(self.test_trainee)
        new_trainee.username = "testUsername"

        # Remove testUsername
        while self.database.get_trainee_by_username(new_trainee.username) is not None:
            db_user = self.database.get_trainee_by_username(
                new_trainee.username)
            self.database.remove_trainee(db_user._id)

        # Get database testUsername trainer
        database_trainee = self.database.get_trainee_by_username(
            new_trainee.username)
        self.assertTrue(database_trainee is None)

        # Add a new trainer
        self.database.add_trainee(new_trainee)

        # Get database testUsername trainer
        database_trainee = self.database.get_trainee_by_username(
            new_trainee.username)
        self.assertTrue(database_trainee is not None)

        # Remove newly added trainer
        self.database.remove_trainee(database_trainee._id)
        database_trainee = self.database.get_trainee_by_username(
            new_trainee.username)
        self.assertTrue(database_trainee is None)

    def test_set_trainee_username(self):
        new_trainee = deepcopy(self.test_trainee)

        # Geting the new user by their username
        db_user_1 = self.database.get_trainee_by_username(
            new_trainee.username)

        # Setting our current user object's id as mongodb id
        new_trainee._id = db_user_1._id

        # Need to hash new_trainee's password
        new_trainee.password = password_sha256(new_trainee.password)

        # Checking if user objects are the same through their dicts
        self.assertTrue(db_user_1.as_dict() == new_trainee.as_dict())

        # Changing new trainee's name to 'elijah'
        new_trainee.username = "elijah"
        self.database.set_trainee_username(
            new_trainee._id, new_trainee.username)

        # Checking if database updated
        db_user_2 = self.database.get_trainee_by_id(new_trainee._id)

        self.assertTrue(db_user_2.as_dict() == new_trainee.as_dict())

        # Removing temp user from database
        self.database.remove_trainee(db_user_2._id)
        self.assertTrue(self.database.get_trainee_by_id(db_user_2._id) is None)

    def test_set_trainee_password(self):

        new_trainee = deepcopy(self.test_trainee)

        # Updating user object to database user
        new_trainee = self.database.get_trainee_by_username(
            new_trainee.username)

        # Changing password
        new_trainee.password = "newPassword"
        self.database.set_trainee_password(
            new_trainee._id, new_trainee.password)

        # Checking password
        db_user = self.database.get_trainee_by_username(
            new_trainee.username)
        new_trainee.password = password_sha256(new_trainee.password)
        self.assertTrue(db_user.password == new_trainee.password)

        self.database.remove_trainee(db_user._id)
        self.assertTrue(
            self.database.get_trainee_by_id(db_user._id) is None)

    def test_set_trainee_location(self):
        new_trainee = deepcopy(self.test_trainee)

        # Updating user object to database user
        new_trainee = self.database.get_trainee_by_username(
            new_trainee.username)

        # Changing location
        new_trainee.location = "newLocation"
        self.database.set_trainee_location(
            new_trainee._id, new_trainee.location)

        # Checking location
        db_user = self.database.get_trainee_by_username(
            new_trainee.username)
        self.assertTrue(db_user.location == new_trainee.location)

        self.database.remove_trainee(db_user._id)
        self.assertTrue(
            self.database.get_trainee_by_id(db_user._id) is None)

    def test_set_trainee_phone(self):
        new_trainee = deepcopy(self.test_trainee)

        # Updating user object to database user
        new_trainee = self.database.get_trainee_by_username(
            new_trainee.username)

        # Changing phone
        new_trainee.phone = "newPhone"
        self.database.set_trainee_phone(new_trainee._id, new_trainee.phone)

        # Checking phone
        db_user = self.database.get_trainee_by_username(
            new_trainee.username)
        self.assertTrue(db_user.phone == new_trainee.phone)

        self.database.remove_trainee(db_user._id)
        self.assertTrue(
            self.database.get_trainee_by_id(db_user._id) is None)

    def test_set_trainee_name(self):
        new_trainee = deepcopy(self.test_trainee)

        # Updating user object to database user
        new_trainee = self.database.get_trainee_by_username(
            new_trainee.username)

        # Changing name
        new_trainee.name = "newname"
        self.database.set_trainee_name(
            new_trainee._id, new_trainee.name)

        # Checking name
        db_user = self.database.get_trainee_by_username(
            new_trainee.username)
        self.assertTrue(db_user.name == new_trainee.name)

        self.database.remove_trainee(db_user._id)
        self.assertTrue(
            self.database.get_trainee_by_username(db_user._id) is None)

    def test_list_trainers_by_search(self):
        # Searching for testTrainer with input "testTrain"
        found_trainers = self.database.list_trainers_by_search("testTrain")
        self.assertEqual(len(found_trainers), 1)

        trainer = self.database.get_trainer_by_username("testTrainer")
        self.assertEqual(found_trainers[0].as_dict(), trainer.as_dict())

    """ Test trainer """

    def test_add_trainer(self):

        # Raise exception if 'testTrainee' username found
        with self.assertRaises(UsernameTakenError):
            new_trainer = deepcopy(self.test_trainer)
            new_trainer.username = "testTrainee"
            self.database.add_trainer(new_trainer)

        # Raise exception if 'testTrainer' username found
        with self.assertRaises(UsernameTakenError):
            new_trainer = deepcopy(self.test_trainer)
            new_trainer.username = "testTrainer"
            self.database.add_trainer(new_trainer)

        # Copy test_trainer and change to unused trainer name
        new_trainer = deepcopy(self.test_trainer)
        new_trainer.username = "testUsername"

        # Remove testUsername
        while self.database.get_trainer_by_username(new_trainer.username) is not None:
            db_user = self.database.get_trainer_by_username(
                new_trainer.username)
            self.database.remove_trainer(db_user._id)

        # Get database testUsername trainer
        database_trainer = self.database.get_trainer_by_username(
            new_trainer.username)
        self.assertTrue(database_trainer is None)

        # Add a new trainer
        self.database.add_trainer(new_trainer)

        # Get database testUsername trainer
        database_trainer = self.database.get_trainer_by_username(
            new_trainer.username)
        self.assertTrue(database_trainer is not None)

        # Remove newly added trainer
        self.database.remove_trainer(database_trainer._id)
        database_trainer = self.database.get_trainer_by_username(
            new_trainer.username)
        self.assertTrue(database_trainer is None)

    def test_set_trainer_username(self):

        new_trainer = deepcopy(self.test_trainer)

        # Geting the new user by their username
        db_user_1 = self.database.get_trainer_by_username(
            new_trainer.username)

        # Setting our current user object's id as mongodb id
        new_trainer._id = db_user_1._id

        # Need to hash new_trainer's password
        new_trainer.password = password_sha256(new_trainer.password)

        # Checking if user objects are the same through their dicts
        self.assertTrue(db_user_1.as_dict() == new_trainer.as_dict())

        # Changing new trainer's name to 'elijah'
        new_trainer.username = "elijah"
        self.database.set_trainer_username(
            new_trainer._id, new_trainer.username)

        # Checking if database updated
        db_user_2 = self.database.get_trainer_by_id(new_trainer._id)

        self.assertTrue(db_user_2.as_dict() == new_trainer.as_dict())

        # Removing temp user from database
        self.database.remove_trainer(db_user_2._id)
        self.assertTrue(self.database.get_trainer_by_id(db_user_2._id) is None)

    def test_set_trainer_password(self):

        new_trainer = deepcopy(self.test_trainer)

        # Updating user object to database user
        new_trainer = self.database.get_trainer_by_username(
            new_trainer.username)

        # Changing password
        new_trainer.password = "newPassword"
        self.database.set_trainer_password(
            new_trainer._id, new_trainer.password)

        # Checking password
        db_user = self.database.get_trainer_by_username(
            new_trainer.username)
        self.assertTrue(db_user.password ==
                        password_sha256(new_trainer.password))

        self.database.remove_trainer(db_user._id)
        self.assertTrue(
            self.database.get_trainer_by_id(db_user._id) is None)

    def test_set_trainer_location(self):

        new_trainer = deepcopy(self.test_trainer)

        # Updating user object to database user
        new_trainer = self.database.get_trainer_by_username(
            new_trainer.username)

        # Changing location
        new_trainer.location = "newLocation"
        self.database.set_trainer_location(
            new_trainer._id, new_trainer.location)

        # Checking location
        db_user = self.database.get_trainer_by_username(
            new_trainer.username)
        self.assertTrue(db_user.location == new_trainer.location)

        self.database.remove_trainer(db_user._id)
        self.assertTrue(
            self.database.get_trainer_by_id(db_user._id) is None)

    def test_set_trainer_phone(self):

        new_trainer = deepcopy(self.test_trainer)

        # Updating user object to database user
        new_trainer = self.database.get_trainer_by_username(
            new_trainer.username)

        # Changing phone
        new_trainer.phone = "newPhone"
        self.database.set_trainer_phone(new_trainer._id, new_trainer.phone)

        # Checking phone
        db_user = self.database.get_trainer_by_username(
            new_trainer.username)
        self.assertTrue(db_user.phone == new_trainer.phone)

        self.database.remove_trainer(db_user._id)
        self.assertTrue(
            self.database.get_trainer_by_id(db_user._id) is None)

    def test_set_trainer_name(self):

        new_trainer = deepcopy(self.test_trainer)

        # Updating user object to database user
        new_trainer = self.database.get_trainer_by_username(
            new_trainer.username)

        # Changing name
        new_trainer.name = "newname"
        self.database.set_trainer_name(
            new_trainer._id, new_trainer.name)

        # Checking name
        db_user = self.database.get_trainer_by_username(
            new_trainer.username)
        self.assertTrue(db_user.name == new_trainer.name)

        self.database.remove_trainer(db_user._id)
        self.assertTrue(
            self.database.get_trainer_by_username(db_user._id) is None)

    """Workout tests"""

    def test_workout_dict_to_class(self):
        new_workout = deepcopy(self.test_workout)

        # Get workout from database
        database_workout = self.database.workout_dict_to_class(
            new_workout.as_dict())

        # Need to pass in the mongo id
        new_workout._id = database_workout._id

        # Check if equal
        self.assertTrue(new_workout.as_dict() == database_workout.as_dict())

    def test_get_workout_class_by_id(self):
        new_workout = deepcopy(self.test_workout)

        # Get workout from database
        database_workout = self.database.get_workout_class_by_name(
            new_workout.name)

        # Need to pass in the mongo id
        new_workout._id = database_workout._id

        # Check if workouts are the same
        self.assertTrue(new_workout.as_dict() == database_workout.as_dict())

        # Get workout from database by id this time
        database_workout = self.database.get_workout_class_by_id(
            new_workout._id)

        # Check if workouts are the same
        self.assertTrue(new_workout.as_dict() == database_workout.as_dict())

    def test_get_workout_class_by_name(self):
        new_workout = deepcopy(self.test_workout)

        # Get workout from database
        database_workout = self.database.get_workout_class_by_name(
            new_workout.name)

        # Need to pass in the mongo id
        new_workout._id = database_workout._id

        # Check if workouts are the same
        self.assertTrue(new_workout.as_dict() == database_workout.as_dict())

    def test_set_workout_creator_id(self):
        new_workout = deepcopy(self.test_workout)

        # Get workout from database
        database_workout = self.database.get_workout_class_by_name(
            new_workout.name)

        # Get trainee from database
        database_trainee = self.database.get_trainee_by_username(
            self.test_trainee.username)

        # Get trainer from database
        database_trainer = self.database.get_trainer_by_username(
            self.test_trainer.username)

        # Need to pass in the mongo id
        new_workout._id = database_workout._id

        # Check if workouts are the same
        self.assertTrue(new_workout.as_dict() == database_workout.as_dict())

        # Make creator id == trainee id
        new_workout.creator_id = database_trainee._id
        self.database.set_workout_creator_id(
            new_workout._id, database_trainee._id)

        # Get workout from database
        database_workout = self.database.get_workout_class_by_name(
            new_workout.name)

        self.assertTrue(new_workout.as_dict() == database_workout.as_dict())

        # Make creator id == trainer id
        new_workout.creator_id = database_trainer._id
        self.database.set_workout_creator_id(
            new_workout._id, database_trainer._id)

        # Get workout from database
        database_workout = self.database.get_workout_class_by_name(
            new_workout.name)

        self.assertTrue(new_workout.as_dict() == database_workout.as_dict())

    def test_set_workout_name(self):
        new_workout = deepcopy(self.test_workout)

        # Get workout from database
        database_workout = self.database.get_workout_class_by_name(
            new_workout.name)

        # Get id and change name
        new_workout._id = database_workout._id
        new_workout.name = "newname"

        # Set it in database
        self.database.set_workout_name(new_workout._id, new_workout.name)

        # Get workout from database
        database_workout = self.database.get_workout_class_by_name(
            new_workout.name)

        self.assertTrue(database_workout.as_dict() == new_workout.as_dict())

        # Removing workout since we changed name. Teardown wont do it
        self.database.remove_workout(new_workout._id)

    def test_set_workout_difficulty(self):
        new_workout = deepcopy(self.test_workout)

        # Get workout from database
        database_workout = self.database.get_workout_class_by_name(
            new_workout.name)

        # Get id and change name
        new_workout._id = database_workout._id
        new_workout.difficulty = "newdifficulty"

        # Set it in database
        self.database.set_workout_difficulty(
            new_workout._id, new_workout.difficulty)

        # Get workout from database
        database_workout = self.database.get_workout_class_by_name(
            new_workout.name)

        self.assertTrue(database_workout.as_dict() == new_workout.as_dict())

    def test_set_workout_about(self):
        new_workout = deepcopy(self.test_workout)

        # Get workout from database
        database_workout = self.database.get_workout_class_by_name(
            new_workout.name)

        # Get id and change name
        new_workout._id = database_workout._id
        new_workout.about = "newabout"

        # Set it in database
        self.database.set_workout_about(new_workout._id, new_workout.about)

        # Get workout from database
        database_workout = self.database.get_workout_class_by_name(
            new_workout.name)

        self.assertTrue(database_workout.as_dict() == new_workout.as_dict())

    def test_set_workout_exp(self):
        new_workout = deepcopy(self.test_workout)

        # Get workout from database
        database_workout = self.database.get_workout_class_by_name(
            new_workout.name)

        # Get id and change name
        new_workout._id = database_workout._id
        new_workout.exp = "newexp"

        # Set it in database
        self.database.set_workout_exp(new_workout._id, new_workout.exp)

        # Get workout from database
        database_workout = self.database.get_workout_class_by_name(
            new_workout.name)

        self.assertTrue(database_workout.as_dict() == new_workout.as_dict())

    def test_remove_workout(self):
        new_workout = deepcopy(self.test_workout)
        new_workout.name = "goingtoremove"

        # Adding workout to database
        self.database.add_workout(new_workout)

        # Get workout from database
        database_workout = self.database.get_workout_class_by_name(
            new_workout.name)

        # Get id and change name
        new_workout._id = database_workout._id

        self.assertTrue(database_workout.as_dict() == new_workout.as_dict())

        self.database.remove_workout(new_workout._id)

        self.assertTrue(self.database.get_workout_class_by_name(
            new_workout.name) is None)

    def test_add_workout(self):
        new_trainee = self.database.get_trainee_by_username(
            self.test_trainee.username)

        new_workout = deepcopy(self.test_workout)

        # Getting the workout by their name
        db_workout = self.database.get_workout_class_by_name(
            self.test_workout.name)

        # Set ids
        new_workout._id = db_workout._id
        new_workout.creator_id = new_trainee._id
        db_workout.creator_id = new_workout.creator_id
        self.assertTrue(new_trainee._id == new_workout.creator_id)
        self.assertTrue(db_workout.as_dict() == new_workout.as_dict())

        # Removing temp workout from database
        self.database.remove_workout(new_workout._id)
        self.assertTrue(
            self.database.get_workout_class_by_id(db_workout._id) is None)

        # Removing temp user from database
        self.database.remove_trainee(new_trainee._id)
        self.assertTrue(self.database.get_trainee_by_id(
            new_trainee._id) is None)

        # Testing to see if an error occurs if adding a workout with no creator id
        new_workout = deepcopy(self.test_workout)
        new_workout.creator_id = None
        with self.assertRaises(WorkoutCreatorIdNotFound):
            self.database.add_workout(new_workout)
