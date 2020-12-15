import unittest
from copy import deepcopy
from bson.objectid import ObjectId
from vitality.database import *
from vitality.trainee import Trainee
from vitality.trainer import Trainer
from vitality.workout import Workout
from vitality.settings import MONGO_URI


class TestDatabase(unittest.TestCase):

    # Creating database object
    database = Database(MONGO_URI)

    # Creating new Trainee object
    test_trainee = Trainee(
        _id=None,
        username="testtrainee",
        password="password",
        name="first last",
        location="Earth",
        phone=1234567890,
        trainers=[])

    # Creating new Trainer object
    test_trainer = Trainer(
        _id=None,
        username="testtrainer",
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
        is_complete=False)

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
        # Remove test Workout if found
        self.database.mongo.workout.delete_many(
            {'name': self.test_workout.name})

        # Removing a test workout
        self.database.mongo.workout.delete_many({'name': 'goingtoremove'})

        # Remove test Trainee if found
        self.database.mongo.trainee.delete_many({
            'username': self.test_trainee.username
        })

        # Remove test Trainer if found
        self.database.mongo.trainer.delete_many({
            'username': self.test_trainer.username
        })

    def test_password_sha256(self):
        password = 'asupersecretpassword'
        hashed_password = '009e3e71eed006baa4441cdc417e58f72a635e52f814400e6301881620628d8b'
        self.assertTrue(password_sha256(password) == hashed_password)

    """Trainee tests"""

    def test_trainee_add_trainer(self):

        trainee = self.database.get_trainee_by_username('testtrainee')
        trainer = self.database.get_trainer_by_username('testtrainer')

        with self.assertRaises(UserNotFoundError):
            self.database.trainee_add_trainer("123456789012345678901234",
                                              trainer._id)

        with self.assertRaises(UserNotFoundError):
            self.database.trainee_add_trainer(trainee._id,
                                              "123456789012345678901234")

        self.database.trainee_add_trainer(trainee._id, trainer._id)

        assert ObjectId(trainer._id) in self.database.mongo.trainee.find_one({
            '_id': ObjectId(trainee._id)
        })['trainers']

    def test_trainer_add_trainee(self):

        trainee = self.database.get_trainee_by_username('testtrainee')
        trainer = self.database.get_trainer_by_username('testtrainer')

        with self.assertRaises(UserNotFoundError):
            self.database.trainer_add_trainee("123456789012345678901234",
                                              trainee._id)

        with self.assertRaises(UserNotFoundError):
            self.database.trainer_add_trainee(trainer._id,
                                              "123456789012345678901234")

        self.database.trainer_add_trainee(trainer._id, trainee._id)

        assert ObjectId(trainee._id) in self.database.mongo.trainer.find_one({
            '_id': ObjectId(trainer._id)
        })['trainees']

    def test_add_trainee(self):

        # Raise exception if 'testTrainee' username found
        with self.assertRaises(UsernameTakenError):
            new_trainer = deepcopy(self.test_trainer)
            new_trainer.username = "testtrainee"
            self.database.add_trainee(new_trainer)

        # Raise exception if 'testTrainer' username found
        with self.assertRaises(UsernameTakenError):
            new_trainer = deepcopy(self.test_trainer)
            new_trainer.username = "testtrainer"
            self.database.add_trainee(new_trainer)

        # Copy test_trainer and change to unused trainer name
        new_trainee = deepcopy(self.test_trainee)
        new_trainee.username = "testusername"

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
        found_trainers = self.database.list_trainers_by_search("testtrain")
        self.assertEqual(len(found_trainers), 1)

        trainer = self.database.get_trainer_by_username("testtrainer")
        self.assertEqual(found_trainers[0].as_dict(), trainer.as_dict())

    def test_list_trainees_by_search(self):
        # Searching for testTrainee with input "testTrain"
        found_trainees = self.database.list_trainees_by_search("testtrain")
        self.assertEqual(len(found_trainees), 1)

        trainee = self.database.get_trainee_by_username("testtrainee")
        self.assertEqual(found_trainees[0].as_dict(), trainee.as_dict())

    """ Test trainer """

    def test_add_trainer(self):

        # Raise exception if 'testTrainee' username found
        with self.assertRaises(UsernameTakenError):
            new_trainer = deepcopy(self.test_trainer)
            new_trainer.username = "testtrainee"
            self.database.add_trainer(new_trainer)

        # Raise exception if 'testTrainer' username found
        with self.assertRaises(UsernameTakenError):
            new_trainer = deepcopy(self.test_trainer)
            new_trainer.username = "testtrainer"
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
        trainee = self.database.get_trainee_by_username(
            self.test_trainee.username)

        # Get workout from database
        database_workout = self.database.get_workout_by_attributes(name=new_workout.name,
                                                                   creator_id=trainee._id)

        # Need to pass in the mongo id
        new_workout._id = database_workout._id

        # Check if workouts are the same
        self.assertTrue(new_workout.as_dict() == database_workout.as_dict())

        # Get workout from database by id this time
        database_workout = self.database.get_workout_by_id(new_workout._id)

        # Check if workouts are the same
        self.assertTrue(new_workout.as_dict() == database_workout.as_dict())

    def test_get_workout_class_by_name(self):
        new_workout = deepcopy(self.test_workout)

        # Get workout from database
        trainee = self.database.get_trainee_by_username(
            self.test_trainee.username)

        # Get workout from database
        database_workout = self.database.get_workout_by_attributes(name=new_workout.name,
                                                                   creator_id=trainee._id)

        # Need to pass in the mongo id
        new_workout._id = database_workout._id

        # Check if workouts are the same
        self.assertTrue(new_workout.as_dict() == database_workout.as_dict())

        self.database.remove_workout(database_workout._id)

    def test_set_workout_creator_id(self):

        try:
            new_workout = deepcopy(self.test_workout)

            # Get trainee from database
            trainee = self.database.get_trainee_by_username(
                self.test_trainee.username)

            # Get trainer from database
            trainer = self.database.get_trainer_by_username(
                self.test_trainer.username)

            database_workout = self.database.get_workout_by_attributes(name=new_workout.name,
                                                                       creator_id=trainee._id)
            assert database_workout is not None

            # Set to trainer id
            self.database.set_workout_creator_id(database_workout._id,
                                                 trainer._id)

            # Get back the new workout
            database_workout = self.database.get_workout_by_attributes(name=new_workout.name,
                                                                       creator_id=trainer._id)
            assert database_workout is not None

            # Check that the creator_id is now changed
            assert database_workout.creator_id == trainer._id

        finally:
            trainer = self.database.get_trainer_by_username(
                self.test_trainer.username)
            self.database.mongo.workout.delete_many({
                'creator_id': ObjectId(trainer._id)
            })

    def test_set_workout_name(self):
        try:
            new_workout = deepcopy(self.test_workout)
            trainee = self.database.get_trainee_by_username(
                self.test_trainee.username)

            self.database.mongo.workout.delete_many(
                {
                    'name': "newname",
                    'creator_id': trainee._id
                }
            )

            # Get workout from database
            database_workout = self.database.get_workout_by_attributes(name=new_workout.name,
                                                                       creator_id=trainee._id)

            # Get id and change name
            new_workout._id = database_workout._id
            new_workout.name = "newname"
            new_workout.creator_id = database_workout.creator_id

            # Set it in database
            self.database.set_workout_name(new_workout._id, new_workout.name)

            # Get workout from database
            database_workout = self.database.get_workout_by_attributes(name=new_workout.name,
                                                                       creator_id=trainee._id)
            self.assertTrue(database_workout.as_dict()
                            == new_workout.as_dict())

            # Removing workout since we changed name. Teardown wont do it
            self.database.remove_workout(new_workout._id)

        finally:
            self.database.mongo.workout.delete_many(
                {
                    'creator_id': trainee._id
                }
            )

    def test_set_workout_difficulty(self):
        new_workout = deepcopy(self.test_workout)

        # Get workout from database
        trainee = self.database.get_trainee_by_username(
            self.test_trainee.username)

        # Get workout from database
        database_workout = self.database.get_workout_by_attributes(name=new_workout.name,
                                                                   creator_id=trainee._id)

        # Get id and change name
        new_workout._id = database_workout._id
        new_workout.difficulty = "newdifficulty"

        # Set it in database
        self.database.set_workout_difficulty(
            new_workout._id, new_workout.difficulty)

        # Get workout from database
        database_workout = self.database.get_workout_by_attributes(name=new_workout.name,
                                                                   creator_id=trainee._id)

        self.assertTrue(database_workout.as_dict() == new_workout.as_dict())

    def test_set_workout_about(self):
        new_workout = deepcopy(self.test_workout)

        # Get workout from database
        trainee = self.database.get_trainee_by_username(
            self.test_trainee.username)

        # Get workout from database
        database_workout = self.database.get_workout_by_attributes(name=new_workout.name,
                                                                   creator_id=trainee._id)

        # Get id and change name
        new_workout._id = database_workout._id
        new_workout.about = "newabout"

        # Set it in database
        self.database.set_workout_about(new_workout._id, new_workout.about)

        # Get workout from database
        database_workout = self.database.get_workout_by_attributes(name=new_workout.name,
                                                                   creator_id=trainee._id)

        self.assertTrue(database_workout.as_dict() == new_workout.as_dict())

    def test_remove_workout(self):
        new_workout = deepcopy(self.test_workout)
        new_workout.name = "goingtoremove"

        # Adding workout to database
        self.database.add_workout(new_workout)

        # Get workout from database
        trainee = self.database.get_trainee_by_username(
            self.test_trainee.username)

        # Get workout from database
        database_workout = self.database.get_workout_by_attributes(name=new_workout.name,
                                                                   creator_id=trainee._id)

        # Get id and change name
        new_workout._id = database_workout._id
        new_workout.creator_id = database_workout.creator_id

        self.assertTrue(database_workout.as_dict() == new_workout.as_dict())
        self.database.remove_workout(new_workout._id)

        with self.assertRaises(WorkoutNotFound):
            self.database.get_workout_by_attributes(name=new_workout.name,
                                                                    creator_id=trainee._id)

    def test_add_workout(self):
        new_trainee = self.database.get_trainee_by_username(
            self.test_trainee.username)

        new_workout = deepcopy(self.test_workout)

        # Getting the workout by their name
        trainee = self.database.get_trainee_by_username(
            self.test_trainee.username)

        # Get workout from database
        database_workout = self.database.get_workout_by_attributes(name=new_workout.name,
                                                                   creator_id=trainee._id)

        # Set ids
        new_workout._id = database_workout._id
        new_workout.creator_id = new_trainee._id
        database_workout.creator_id = new_workout.creator_id
        self.assertTrue(new_trainee._id == new_workout.creator_id)
        self.assertTrue(database_workout.as_dict() == new_workout.as_dict())

        # Removing temp workout from database
        self.database.remove_workout(new_workout._id)
        self.assertTrue(
            self.database.get_workout_by_id(database_workout._id) is None)

        # Removing temp user from database
        self.database.remove_trainee(new_trainee._id)
        self.assertTrue(self.database.get_trainee_by_id(
            new_trainee._id) is None)

        # Testing to see if an error occurs if adding a workout with no creator id
        new_workout = deepcopy(self.test_workout)
        new_workout.creator_id = None
        with self.assertRaises(WorkoutCreatorIdNotFoundError):
            self.database.add_workout(new_workout)

    def test_remove_trainee(self):

        try:
            self.database.add_trainee(Trainee(_id=None,
                                              username="testtrainee1",
                                              password="pass",
                                              name="testTrainee1",
                                              location="somewhere",
                                              phone=1234567890))
            self.database.add_trainee(Trainee(_id=None,
                                              username="testtrainee2",
                                              password="pass",
                                              name="testTrainee2",
                                              location="somewhere",
                                              phone=1234567890))
            self.database.add_trainee(Trainee(_id=None,
                                              username="testtrainee3",
                                              password="pass",
                                              name="testTrainee3",
                                              location="somewhere",
                                              phone=1234567890))

            self.database.add_trainer(Trainer(_id=None,
                                              username="testtrainer1",
                                              password="pass",
                                              name="testTrainer3",
                                              location="somewhere",
                                              phone=1234567890))

            trainee1_id = str(self.database.mongo.trainee.find_one(
                {'username': 'testtrainee1'})['_id'])
            trainee2_id = str(self.database.mongo.trainee.find_one(
                {'username': 'testtrainee2'})['_id'])
            trainee3_id = str(self.database.mongo.trainee.find_one(
                {'username': 'testtrainee3'})['_id'])
            trainer_id = str(self.database.mongo.trainer.find_one(
                {'username': 'testtrainer1'})['_id'])

            assert self.database.get_trainer_by_username(
                "testtrainer1") is not None
            assert self.database.get_trainee_by_username(
                "testtrainee1") is not None
            assert self.database.get_trainee_by_username(
                "testtrainee2") is not None
            assert self.database.get_trainee_by_username(
                "testtrainee3") is not None

            self.database.trainer_add_trainee(trainer_id, trainee1_id)
            self.database.trainer_add_trainee(trainer_id, trainee2_id)
            self.database.trainer_add_trainee(trainer_id, trainee3_id)

            assert len(self.database.get_trainer_by_id(
                trainer_id).trainees) == 3

            self.database.remove_trainee(trainee1_id)
            assert len(self.database.get_trainer_by_id(
                trainer_id).trainees) == 2

            self.database.remove_trainee(trainee2_id)
            assert len(self.database.get_trainer_by_id(
                trainer_id).trainees) == 1

            self.database.remove_trainee(trainee3_id)
            assert len(self.database.get_trainer_by_id(
                trainer_id).trainees) == 0

        finally:
            self.database.mongo.trainee.delete_many(
                {"username": "testtrainee1"})
            self.database.mongo.trainee.delete_many(
                {"username": "testtrainee2"})
            self.database.mongo.trainee.delete_many(
                {"username": "testtrainee3"})
            self.database.mongo.trainer.delete_many(
                {"username": "testTrainer1"})

    def test_remove_trainee(self):

        try:
            self.database.add_trainer(Trainer(_id=None,
                                              username="testtrainer1",
                                              password="pass",
                                              name="testTrainer1",
                                              location="somewhere",
                                              phone=1234567890))
            self.database.add_trainer(Trainer(_id=None,
                                              username="testtrainer2",
                                              password="pass",
                                              name="testTrainer2",
                                              location="somewhere",
                                              phone=1234567890))
            self.database.add_trainer(Trainer(_id=None,
                                              username="testtrainer3",
                                              password="pass",
                                              name="testTrainer3",
                                              location="somewhere",
                                              phone=1234567890))

            self.database.add_trainee(Trainee(_id=None,
                                              username="testtrainee1",
                                              password="pass",
                                              name="testTrainer3",
                                              location="somewhere",
                                              phone=1234567890))

            trainer1_id = str(self.database.mongo.trainer.find_one(
                {'username': 'testtrainer1'})['_id'])
            trainer2_id = str(self.database.mongo.trainer.find_one(
                {'username': 'testtrainer2'})['_id'])
            trainer3_id = str(self.database.mongo.trainer.find_one(
                {'username': 'testtrainer3'})['_id'])
            trainee_id = str(self.database.mongo.trainee.find_one(
                {'username': 'testtrainee1'})['_id'])

            assert self.database.get_trainee_by_username(
                "testtrainee1") is not None
            assert self.database.get_trainer_by_username(
                "testtrainer1") is not None
            assert self.database.get_trainer_by_username(
                "testtrainer2") is not None
            assert self.database.get_trainer_by_username(
                "testtrainer3") is not None

            self.database.trainee_add_trainer(trainee_id, trainer1_id)
            self.database.trainee_add_trainer(trainee_id, trainer2_id)
            self.database.trainee_add_trainer(trainee_id, trainer3_id)

            assert len(self.database.get_trainee_by_id(
                trainee_id).trainers) == 3

            self.database.remove_trainer(trainer1_id)
            assert len(self.database.get_trainee_by_id(
                trainee_id).trainers) == 2

            self.database.remove_trainer(trainer2_id)
            assert len(self.database.get_trainee_by_id(
                trainee_id).trainers) == 1

            self.database.remove_trainer(trainer3_id)
            assert len(self.database.get_trainee_by_id(
                trainee_id).trainers) == 0

        finally:
            self.database.mongo.trainer.delete_many(
                {"username": "testtrainer1"})
            self.database.mongo.trainer.delete_many(
                {"username": "testtrainer2"})
            self.database.mongo.trainer.delete_many(
                {"username": "testtrainer3"})
            self.database.mongo.trainee.delete_many(
                {"username": "testtrainee1"})

    def test_get_all_workouts_by_creatorid(self):

        # Checking if workout total is equal to 1
        trainee = self.database.get_trainee_by_username(
            self.test_trainee.username)
        workouts = self.database.get_all_workouts_by_creatorid(trainee._id)
        assert len(workouts) == 1

        new_workout = Workout(
            _id=None,
            creator_id=trainee._id,
            name="goingtoremove",  # tearDown removes all of these
            difficulty="novice",
            about="something something else"
        )

        self.database.add_workout(new_workout)
        workouts = self.database.get_all_workouts_by_creatorid(trainee._id)
        assert len(workouts) == 2

    """Invitation tests"""

    def test_create_invitation(self):
        """Testing invitation creation"""

        def clean_up(user_one, user_two):
            # Clean up
            self.database.mongo.invitation.delete_many({
                'sender': ObjectId(user_one._id)
            })
            self.database.mongo.invitation.delete_many({
                'recipient': ObjectId(user_one._id)
            })
            self.database.mongo.invitation.delete_many({
                'sender': ObjectId(user_two._id)
            })
            self.database.mongo.invitation.delete_many({
                'recipient': ObjectId(user_two._id)
            })

        try:
            trainee = self.database.get_trainee_by_username('testtrainee')
            trainer = self.database.get_trainer_by_username('testtrainer')

            clean_up(trainee, trainer)

            invitation_id = self.database.create_invitation(trainee._id,
                                                            trainer._id)
            database_invitation = self.database.mongo.invitation.find_one({
                'sender': ObjectId(trainee._id),
                'recipient': ObjectId(trainer._id)
            })

            assert invitation_id is not None
            assert database_invitation is not None
            assert str(database_invitation['_id']) == str(invitation_id)
            assert str(database_invitation['sender']) == trainee._id
            assert str(database_invitation['recipient']) == trainer._id

            # Check if non-existent user throws error
            with self.assertRaises(UserNotFoundError):
                self.database.create_invitation('000000000000000000000000',
                                                trainer._id)

            with self.assertRaises(UserNotFoundError):
                self.database.create_invitation(trainee._id,
                                                '000000000000000000000000')
        finally:
            clean_up(trainee, trainer)

    def test_delete_invitation(self):
        """Testing invitation deletion"""
        def clean_up(user_one, user_two):
            # Clean up
            self.database.mongo.invitation.delete_many({
                'sender': ObjectId(user_one._id)
            })
            self.database.mongo.invitation.delete_many({
                'recipient': ObjectId(user_one._id)
            })
            self.database.mongo.invitation.delete_many({
                'sender': ObjectId(user_two._id)
            })
            self.database.mongo.invitation.delete_many({
                'recipient': ObjectId(user_two._id)
            })
        try:
            trainee = self.database.get_trainee_by_username('testtrainee')
            trainer = self.database.get_trainer_by_username('testtrainer')
            clean_up(trainee, trainer)

            invitation = self.database.mongo.invitation.insert_one({
                'sender': ObjectId(trainee._id),
                'recipient': ObjectId(trainer._id)
            })
            self.database.delete_invitation(invitation.inserted_id)
            database_invitation = self.database.mongo.invitation.find_one({
                '_id': invitation.inserted_id
            })
            assert database_invitation is None

            database_invitation = self.database.mongo.invitation.find_one({
                'sender': trainee._id,
                'recipient': trainer._id
            })
            assert database_invitation is None
        finally:
            clean_up(trainee, trainer)

    def test_search_invitation(self):
        """Testing invitation search"""

        def clean_up(user_one, user_two):
            # Clean up
            self.database.mongo.invitation.delete_many({
                'sender': ObjectId(user_one._id)
            })
            self.database.mongo.invitation.delete_many({
                'recipient': ObjectId(user_one._id)
            })
            self.database.mongo.invitation.delete_many({
                'sender': ObjectId(user_two._id)
            })
            self.database.mongo.invitation.delete_many({
                'recipient': ObjectId(user_two._id)
            })

        try:
            trainee = self.database.get_trainee_by_username('testtrainee')
            trainer = self.database.get_trainer_by_username('testtrainer')
            clean_up(trainee, trainer)

            with self.assertRaises(InvitationNotFound):
                self.database.search_invitation("000000000000000000000000")

            invitation = self.database.mongo.invitation.insert_one({
                'sender': ObjectId(trainee._id),
                'recipient': ObjectId(trainer._id)
            })
            searched_invitation = self.database.search_invitation(
                invitation.inserted_id)

            assert searched_invitation._id == str(invitation.inserted_id)
            assert searched_invitation.sender == str(trainee._id)
            assert searched_invitation.recipient == str(trainer._id)
        finally:
            clean_up(trainee, trainer)

    def test_search_all_user_invitations(self):
        """Testing the search feature to get all sent and recieved invitations by a user."""

        def clean_up(user_one, user_two):
            # Clean up
            self.database.mongo.invitation.delete_many({
                'sender': ObjectId(user_one._id)
            })
            self.database.mongo.invitation.delete_many({
                'recipient': ObjectId(user_one._id)
            })
            self.database.mongo.invitation.delete_many({
                'sender': ObjectId(user_two._id)
            })
            self.database.mongo.invitation.delete_many({
                'recipient': ObjectId(user_two._id)
            })
        try:
            trainee = self.database.get_trainee_by_username('testtrainee')
            trainer = self.database.get_trainer_by_username('testtrainer')

            clean_up(trainee, trainer)

            invitation = self.database.mongo.invitation.insert_one({
                'sender': ObjectId(trainee._id),
                'recipient': ObjectId(trainer._id)
            })

            all_sent, all_recieved = self.database.search_all_user_invitations(
                trainee._id)
            assert len(all_sent) > 0
            assert len(all_recieved) == 0

            all_sent, all_recieved = self.database.search_all_user_invitations(
                trainer._id)
            assert len(all_recieved) > 0
            assert len(all_sent) == 0

        finally:
            clean_up(trainee, trainer)

    def test_accept_invitation(self):
        """Checking to see that a user can accept a recieved invitation."""
        def clean_up(user_one, user_two):
            # Clean up
            self.database.mongo.invitation.delete_many({
                'sender': ObjectId(user_one._id)
            })
            self.database.mongo.invitation.delete_many({
                'recipient': ObjectId(user_one._id)
            })
            self.database.mongo.invitation.delete_many({
                'sender': ObjectId(user_two._id)
            })
            self.database.mongo.invitation.delete_many({
                'recipient': ObjectId(user_two._id)
            })

        trainee = self.database.get_trainee_by_username('testtrainee')
        trainer = self.database.get_trainer_by_username('testtrainer')

        try:

            clean_up(trainee, trainer)

            invitation = self.database.mongo.invitation.insert_one({
                'sender': ObjectId(trainee._id),
                'recipient': ObjectId(trainer._id)
            })

            with self.assertRaises(InvitationNotFound):
                self.database.accept_invitation('000000000000000000000000',
                                                str(trainee._id))

            assert self.database.mongo.invitation.find_one({
                '_id': ObjectId(invitation.inserted_id)
            }) is not None

            assert self.database.mongo.invitation.find_one({
                'sender': ObjectId(trainee._id)
            }) is not None

            assert self.database.mongo.invitation.find_one({
                'recipient': ObjectId(trainer._id)
            }) is not None

            self.database.accept_invitation(str(invitation.inserted_id),
                                            str(trainer._id))

            assert self.database.mongo.invitation.find_one({
                '_id': invitation.inserted_id
            }) is None

            assert ObjectId(trainee._id) in self.database.mongo.trainer.find_one({
                '_id': ObjectId(trainer._id)
            })['trainees']

            assert ObjectId(trainer._id) in self.database.mongo.trainee.find_one({
                '_id': ObjectId(trainee._id)
            })['trainers']

            clean_up(trainee, trainer)

            invitation = self.database.mongo.invitation.insert_one({
                'sender': ObjectId(trainer._id),
                'recipient': ObjectId(trainee._id)
            })

            with self.assertRaises(InvitationNotFound):
                self.database.accept_invitation('000000000000000000000000',
                                                str(trainer._id))

            assert self.database.mongo.invitation.find_one({
                '_id': ObjectId(invitation.inserted_id)
            }) is not None

            assert self.database.mongo.invitation.find_one({
                'sender': ObjectId(trainer._id)
            }) is not None

            assert self.database.mongo.invitation.find_one({
                'recipient': ObjectId(trainee._id)
            }) is not None

            self.database.accept_invitation(str(invitation.inserted_id),
                                            str(trainee._id))

            assert self.database.mongo.invitation.find_one({
                '_id': invitation.inserted_id
            }) is None

            assert ObjectId(trainee._id) in self.database.mongo.trainer.find_one({
                '_id': ObjectId(trainer._id)
            })['trainees']

            assert ObjectId(trainer._id) in self.database.mongo.trainee.find_one({
                '_id': ObjectId(trainee._id)
            })['trainers']

        finally:
            clean_up(trainee, trainer)

    def test_trainee_remove_trainer(self):
        """Tests to see if a trainee gets removed from a trainers list"""

        trainee = self.database.get_trainee_by_username('testtrainee')
        trainer = self.database.get_trainer_by_username('testtrainer')

        with self.assertRaises(UserNotFoundError):
            self.database.trainee_remove_trainer("123456789012345678901234",
                                                 trainer._id)

        with self.assertRaises(UserNotFoundError):
            self.database.trainee_remove_trainer(trainee._id,
                                                 "123456789012345678901234")

        self.database.mongo.trainee.update_one(
            {"_id": ObjectId(trainee._id)},
            {
                "$addToSet": {
                    "trainers": ObjectId(trainer._id)
                }
            })

        assert ObjectId(trainer._id) in self.database.mongo.trainee.find_one({
            '_id': ObjectId(trainee._id)
        })['trainers']

        self.database.trainee_remove_trainer(trainee._id, trainer._id)

        assert ObjectId(trainer._id) not in self.database.mongo.trainee.find_one({
            '_id': ObjectId(trainee._id)
        })['trainers']

    def test_trainer_remove_trainee(self):
        """Tests to see if a trainee gets removed from a trainers list"""

        trainee = self.database.get_trainee_by_username('testtrainee')
        trainer = self.database.get_trainer_by_username('testtrainer')

        with self.assertRaises(UserNotFoundError):
            self.database.trainer_remove_trainee("123456789012345678901234",
                                                 trainee._id)

        with self.assertRaises(UserNotFoundError):
            self.database.trainer_remove_trainee(trainer._id,
                                                 "123456789012345678901234")

        self.database.mongo.trainer.update_one(
            {"_id": ObjectId(trainer._id)},
            {
                "$addToSet": {
                    "trainees": ObjectId(trainee._id)
                }
            })

        assert ObjectId(trainee._id) in self.database.mongo.trainer.find_one({
            '_id': ObjectId(trainer._id)
        })['trainees']

        self.database.trainer_remove_trainee(trainer._id, trainee._id)

        assert ObjectId(trainee._id) not in self.database.mongo.trainer.find_one({
            '_id': ObjectId(trainer._id)
        })['trainees']
