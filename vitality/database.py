from .trainee import Trainee
from .trainer import Trainer
from .workout import Workout
from bson.objectid import ObjectId
from flask_pymongo import PyMongo
from markupsafe import escape


class Database:
    def __init__(self, app):
        """Constructor for Database class."""
        self.mongo = PyMongo(app)

    """ Trainee Functions """

    def trainee_dict_to_class(self, trainee_dict):
        """Return a Trainee class from a dictionary"""
        return Trainee(
            id=str(trainee_dict['_id']),
            username=trainee_dict['username'],
            password=trainee_dict['password'],
            name=trainee_dict['name'],
            location=trainee_dict['location'],
            phone=trainee_dict['phone']
        )

    def get_trainee_id_by_login(self, username, password):
        """Return the trainer id if login matches"""
        trainee = self.mongo.db.trainee.find_one({
            'username': username,
            'password': password})

        return str(trainee['_id']) if trainee is not None else None

    def get_trainee_class_by_id(self, id):
        """Returns the Trainee class of the User found by the trainee's id."""
        found_user = self.mongo.db.trainee.find_one({"_id": ObjectId(id)})

        if found_user:
            return self.trainee_dict_to_class(found_user)

        return None

    def get_trainee_class_by_username(self, username):
        """Returns the Trainee class of the User found by the trainee's username."""
        found_user = self.mongo.db.trainee.find_one({"username": username})

        if found_user:
            return self.trainee_dict_to_class(found_user)

        return None

    def get_trainee_by_id(self, id):
        """Returns the Trainee class found by the trainee's id."""
        return self.mongo.db.trainee.find_one({"_id": ObjectId(id)})

    def get_trainee_by_username(self, username):
        """Returns the Trainee class found by the trainee's username."""
        return self.mongo.db.trainee.find_one({"username": username})

    def set_trainee_username(self, id, username):
        """Updates a trainee's username given a user id."""
        self.mongo.db.trainee.update_one(
            {"_id": ObjectId(id)},
            {
                "$set": {
                    "username": username
                }
            })

    def set_trainee_password(self, id, password):
        """Updates a trainee's password given a user id."""
        self.mongo.db.trainee.update_one(
            {"_id": ObjectId(id)},
            {
                "$set": {
                    "password": password
                }
            })

    def set_trainee_location(self, id, location):
        """Updates a trainee's location given a user id."""
        self.mongo.db.trainee.update_one(
            {"_id": ObjectId(id)},
            {
                "$set": {
                    "location": location
                }
            })

    def set_trainee_phone(self, id, phone):
        """Updates a trainee's phone number given a user id."""
        self.mongo.db.trainee.update_one(
            {"_id": ObjectId(id)},
            {
                "$set": {
                    "phone": phone
                }
            })

    def set_trainee_name(self, id, name):
        """Updates a trainee's name given a user id."""
        self.mongo.db.trainee.update_one(
            {"_id": ObjectId(id)},
            {
                "$set": {
                    "name": name
                }
            })

    def add_trainee(self, user):
        """Adds a user to the database based on a provided Trainee class."""
        if (self.get_trainee_by_username(user.username)):
            raise UsernameTakenError("Username was taken.")

        self.mongo.db.trainee.insert_one({
            'username': user.username,
            'password': user.password,
            'name': user.name,
            'location': user.location,
            'phone': user.phone})

    def remove_trainee(self, id):
        """Deletes a trainee by trainee id."""
        self.mongo.db.trainee.delete_one({"_id": ObjectId(id)})

    """ Trainer Functions """

    def trainer_dict_to_class(self, trainer_dict):
        """Return a Trainer class from a dictionary"""
        return Trainer(
            id=str(trainer_dict['_id']),
            username=trainer_dict['username'],
            password=trainer_dict['password'],
            name=trainer_dict['name'],
            location=trainer_dict['location'],
            phone=trainer_dict['phone']
        )

    def get_trainer_id_by_login(self, username, password):
        """Return the trainer id if login matches"""
        trainer = self.mongo.db.trainer.find_one({
            'username': username,
            'password': password})

        return str(trainer['_id']) if trainer is not None else None

    def get_trainer_class_by_username(self, username):
        """Returns the trainer class of the trainer found by the trainer's username."""
        found_user = self.mongo.db.trainer.find_one({"username": escape(username)})

        if found_user:
            return self.trainer_dict_to_class(found_user)

        return None

    def get_trainer_class_by_id(self, id):
        """Returns the trainer class of the trainer found by the trainer's id."""
        found_trainer = self.mongo.db.trainer.find_one({"_id": ObjectId(id)})

        if found_trainer:
            return self.trainer_dict_to_class(found_trainer)

        return None

    def get_trainer_by_id(self, id):
        """Returns the trainer class found by the trainer's id."""
        return self.mongo.db.trainer.find_one({"_id": ObjectId(id)})

    def get_trainer_by_username(self, username):
        """Returns the trainer class found by the trainer's username."""
        return self.mongo.db.trainer.find_one({"username": escape(username)})

    def list_trainers_by_search(self, username):
        found_trainers = []

        usernames_found = self.mongo.db.trainer.find({
            "username": {"$regex": r".*{}.*".format(escape(username))}
        })

        if usernames_found is not None:
            found_trainers.extend(usernames_found)

        names_found = self.mongo.db.trainer.find({
            "name": {"$regex": r".*{}.*".format(escape(username))}
        })

        if names_found is not None:
            found_trainers.extend(names_found)

        return found_trainers

    def set_trainer_username(self, id, username):
        """Updates a trainer's username given a trainer id."""
        self.mongo.db.trainer.update_one(
            {"_id": ObjectId(id)},
            {
                "$set": {
                    "username": username
                }
            })

    def set_trainer_password(self, id, password):
        """Updates a trainer's password given a trainer id."""
        self.mongo.db.trainer.update_one(
            {"_id": ObjectId(id)},
            {
                "$set": {
                    "password": password
                }
            })

    def set_trainer_location(self, id, location):
        """Updates a trainer's location given a trainer id."""
        self.mongo.db.trainer.update_one(
            {"_id": ObjectId(id)},
            {
                "$set": {
                    "location": location
                }
            })

    def set_trainer_phone(self, id, phone):
        """Updates a trainer's phone number given a trainer id."""
        self.mongo.db.trainer.update_one(
            {"_id": ObjectId(id)},
            {
                "$set": {
                    "phone": phone
                }
            })

    def set_trainer_name(self, id, name):
        """Updates a trainer's name given a trainer id."""
        self.mongo.db.trainer.update_one(
            {"_id": ObjectId(id)},
            {
                "$set": {
                    "name": name
                }
            })

    def add_trainer(self, trainer):
        """Adds a trainer to the database based on a provided trainer class."""
        if (self.get_trainer_by_username(trainer.username)):
            raise UsernameTakenError("username was taken.")

        self.mongo.db.trainer.insert_one({
            'username': trainer.username,
            'password': trainer.password,
            'name': trainer.name,
            'location': trainer.location,
            'phone': trainer.phone})

    def remove_trainer(self, id):
        """Deletes a trainer by trainer id."""
        self.mongo.db.trainer.delete_one({"_id": ObjectId(id)})

    """Workout Functions"""

    def workout_dict_to_class(self, workout_dict):
        """Takes in a workout dictionary and returns a Workout class"""
        return Workout(
            id=workout_dict['_id'],
            creator_id=workout_dict['creator_id'],
            name=workout_dict['name'],
            difficulty=workout_dict['difficulty'],
            about=workout_dict['about'],
            exp=workout_dict['exp']
        )

    def get_workout_class_by_id(self, id):
        """Returns the Workout class found by the workout's id."""
        found_workout = self.mongo.db.workout.find_one({"_id": ObjectId(id)})

        if found_workout:
            return self.workout_dict_to_class(found_workout)

        return None

    def get_workout_class_by_name(self, name):
        """Returns the Workout class found by the workout's name."""
        found_workout = self.mongo.db.workout.find_one({"name": name})

        if found_workout:
            return self.workout_dict_to_class(found_workout)

        return None

    def set_workout_creator_id(self, id, creator_id):
        """Updates a workout's creator id given a workout id."""
        self.mongo.db.workout.update_one(
            {"_id": ObjectId(id)},
            {
                "$set": {
                    "creator_id": creator_id
                }
            })

    def set_workout_name(self, id, name):
        """Updates a workout's name given a workout id."""
        self.mongo.db.workout.update_one(
            {"_id": ObjectId(id)},
            {
                "$set": {
                    "name": name
                }
            })

    def set_workout_difficulty(self, id, difficulty):
        """Updates a workout's difficulty given a workout id."""
        self.mongo.db.workout.update_one(
            {"_id": ObjectId(id)},
            {
                "$set": {
                    "difficulty": difficulty
                }
            })

    def set_workout_about(self, id, about):
        """Updates a workout's about information given a workout id."""
        self.mongo.db.workout.update_one(
            {"_id": ObjectId(id)},
            {
                "$set": {
                    "about": about
                }
            })

    def set_workout_exp(self, id, exp):
        """Updates a workout's experience points given a workout id."""
        self.mongo.db.workout.update_one(
            {"_id": ObjectId(id)},
            {
                "$set": {
                    "exp": exp
                }
            })

    def remove_workout(self, id):
        """Deletes a workout by workout id."""
        self.mongo.db.workout.delete_one({"_id": ObjectId(id)})

    def add_workout(self, workout):
        """Adds a workout to the database based on a provided Workout class."""

        if self.get_trainee_class_by_id(workout.creator_id) is None or not self.get_trainer_class_by_id(workout.creator_id) is None:
            raise WorkoutCreatorIdNotFound("Creator Id Not Found")

        self.mongo.db.workout.insert_one({
            "creator_id": workout.creator_id,
            'name': workout.name,
            "difficulty": workout.difficulty,
            "about": workout.about,
            "exp": workout.exp})


class UsernameTakenError(ValueError):
    """If a username was taken within the database class"""
    pass


class WorkoutCreatorIdNotFound(AttributeError):
    """Error for when Workout creator id is missing"""
    pass
