from .trainee import Trainee
from .trainer import Trainer
from .workout import Workout
from bson.objectid import ObjectId
from flask_pymongo import PyMongo
from markupsafe import escape
import re
import hashlib


def password_sha256(password: str):
    return hashlib.sha256(escape(password).encode()).hexdigest()


class Database:
    def __init__(self, app):
        """Constructor for Database class."""
        self.mongo = PyMongo(app)

    """ Trainee Functions """

    def trainee_dict_to_class(self, trainee_dict: dict):
        """Return a Trainee class from a dictionary"""
        trainee_dict['_id'] = str(trainee_dict['_id'])
        trainee_dict['trainers'] = [str(trainer_id) for trainer_id in trainee_dict['trainers']]
        # WARNING: Removed converting trainers to classes due to unintended recursion
        return Trainee(**trainee_dict)

    def get_trainee_id_by_login(self, username: str, password: str):
        """
        Return the trainer id if login matches.

        username: str - The user created user name.
        password: str - The user created password hashed in SHA256. 
        """
        trainee = self.mongo.db.trainee.find_one({
            'username': username,
            'password': password})

        return str(trainee['_id']) if trainee is not None else None

    def get_trainee_by_id(self, id: str):
        """Returns the Trainee class of the User found by the trainee's id."""
        found_user = self.mongo.db.trainee.find_one({"_id": ObjectId(id)})

        if found_user:
            return self.trainee_dict_to_class(found_user)

        return None

    def get_trainee_by_username(self, username: str):
        """Returns the Trainee class of the User found by the trainee's username."""
        found_user = self.mongo.db.trainee.find_one({"username": username})

        if found_user:
            return self.trainee_dict_to_class(found_user)

        return None

    def set_trainee_username(self, id: str, username: str):
        """Updates a trainee's username given a user id."""
        self.mongo.db.trainee.update_one(
            {"_id": ObjectId(id)},
            {
                "$set": {
                    "username": username
                }
            })

    def set_trainee_password(self, id: str, password: str):
        """Updates a trainee's password given a user id."""
        self.mongo.db.trainee.update_one(
            {"_id": ObjectId(id)},
            {
                "$set": {
                    "password": password_sha256(password)
                }
            })

    def set_trainee_location(self, id: str, location: str):
        """Updates a trainee's location given a user id."""
        self.mongo.db.trainee.update_one(
            {"_id": ObjectId(id)},
            {
                "$set": {
                    "location": location
                }
            })

    def set_trainee_phone(self, id: str, phone: int):
        """Updates a trainee's phone number given a user id."""
        self.mongo.db.trainee.update_one(
            {"_id": ObjectId(id)},
            {
                "$set": {
                    "phone": phone
                }
            })

    def set_trainee_name(self, id: str, name: str):
        """Updates a trainee's name given a user id."""
        self.mongo.db.trainee.update_one(
            {"_id": ObjectId(id)},
            {
                "$set": {
                    "name": name
                }
            })

    def trainee_add_trainer(self, trainee_id: str, trainer_id: str):
        """Add trainer object id to trainee's trainer list"""
        if self.get_trainee_by_id(trainee_id) is None:
            raise UserNotFoundError("Trainee ID does not exist.")

        if self.get_trainer_by_id(trainer_id) is None:
            raise UserNotFoundError("Trainer ID does not exist.")

        self.mongo.db.trainee.update_one(
            {"_id": ObjectId(trainee_id)},
            {
                "$addToSet": {
                    "trainers": ObjectId(trainer_id)
                }
            })

    def add_trainee(self, trainee: Trainee):
        """Adds a user to the database based on a provided Trainee class."""
        if (self.get_trainee_by_username(trainee.username) is not None):
            raise UsernameTakenError("Username was taken.")

        if (self.get_trainer_by_username(trainee.username) is not None):
            raise UsernameTakenError("Username was taken.")

        trainee_dict = trainee.as_dict()
        trainee_dict.pop('_id', None)
        trainee_dict['password'] = password_sha256(trainee.password)
        self.mongo.db.trainee.insert_one(trainee_dict)

    def remove_trainee(self, id: str):
        """Deletes a trainee by trainee id."""
        self.mongo.db.trainee.delete_one({"_id": ObjectId(id)})

    """ Trainer Functions """

    def trainer_dict_to_class(self, trainer_dict: str):
        """Return a Trainer class from a dictionary"""
        trainer_dict['_id'] = str(trainer_dict['_id'])
        trainer_dict['trainees'] = [str(trainee_id) for trainee_id in trainer_dict['trainees']]
        # WARNING: Removed converting trainees to classes due to unintended recursion
        return Trainer(**trainer_dict)

    def get_trainer_id_by_login(self, username: str, password: str):
        """Return the trainer id if login matches"""
        trainer = self.mongo.db.trainer.find_one({
            'username': username,
            'password': password})

        return str(trainer['_id']) if trainer is not None else None

    def get_trainer_by_username(self, username: str):
        """Returns the trainer class of the trainer found by the trainer's username."""
        found_user = self.mongo.db.trainer.find_one(
            {"username": escape(username)})
        if found_user:
            return self.trainer_dict_to_class(found_user)

        return None

    def get_trainer_by_id(self, id: str):
        """Returns the trainer class of the trainer found by the trainer's id."""
        found_trainer = self.mongo.db.trainer.find_one({"_id": ObjectId(id)})
        if found_trainer:
            return self.trainer_dict_to_class(found_trainer)

        return None

    def list_trainers_by_search(self, name: str):
        """Return a list of trainers by using regex against the 'name' and 'username' fields"""
        def escape_regex(word: str):
            """Escaping the user input being passed into regex"""
            word = escape(word)
            word = re.escape(word)
            return word

        trainers = []

        found_trainers = self.mongo.db.trainer.find(
            {"$or": [
                {
                    "username": {"$regex": r".*{}.*".format(escape_regex(name))}
                },
                {
                    "name": {"$regex": r".*{}.*".format(escape_regex(name))}
                }
            ]}
        )

        if found_trainers is not None:
            for trainer in found_trainers:
                trainers.append(self.trainer_dict_to_class(trainer))

        return trainers

    def list_trainees_by_search(self, name: str):
        """Return a list of trainees by using regex against the 'name' and 'username' fields"""
        def escape_regex(word: str):
            """Escaping the user input being passed into regex"""
            word = escape(word)
            word = re.escape(word)
            return word

        trainees = []
        found_trainees = self.mongo.db.trainee.find(
            {"$or": [
                {
                    "username": {"$regex": r".*{}.*".format(escape_regex(name))}
                },
                {
                    "name": {"$regex": r".*{}.*".format(escape_regex(name))}
                }
            ]}
        )

        if found_trainees is not None:
            for trainee in found_trainees:
                trainees.append(self.trainee_dict_to_class(trainee))

        return trainees

    def set_trainer_username(self, id: str, username: str):
        """Updates a trainer's username given a trainer id."""
        self.mongo.db.trainer.update_one(
            {"_id": ObjectId(id)},
            {
                "$set": {
                    "username": username
                }
            })

    def set_trainer_password(self, id: str, password: str):
        """Updates a trainer's password given a trainer id."""
        self.mongo.db.trainer.update_one(
            {"_id": ObjectId(id)},
            {
                "$set": {
                    "password": password_sha256(password)
                }
            })

    def set_trainer_location(self, id: str, location: str):
        """Updates a trainer's location given a trainer id."""
        self.mongo.db.trainer.update_one(
            {"_id": ObjectId(id)},
            {
                "$set": {
                    "location": location
                }
            })

    def set_trainer_phone(self, id: str, phone: str):
        """Updates a trainer's phone number given a trainer id."""
        self.mongo.db.trainer.update_one(
            {"_id": ObjectId(id)},
            {
                "$set": {
                    "phone": phone
                }
            })

    def set_trainer_name(self, id: str, name: str):
        """Updates a trainer's name given a trainer id."""
        self.mongo.db.trainer.update_one(
            {"_id": ObjectId(id)},
            {
                "$set": {
                    "name": name
                }
            })

    def trainer_add_trainee(self, trainer_id: str, trainee_id: str):
        """Add trainer object id to trainee's trainer list"""
        if self.get_trainee_by_id(trainee_id) is None:
            raise UserNotFoundError("Trainee ID does not exist.")

        if self.get_trainer_by_id(trainer_id) is None:
            raise UserNotFoundError("Trainer ID does not exist.")

        self.mongo.db.trainer.update_one(
            {"_id": ObjectId(trainer_id)},
            {
                "$addToSet": {
                    "trainees": ObjectId(trainee_id)
                }
            })

    def trainer_peak_trainees(self, trainer_id: str):
        """Returns a list of all trainees that have added this trainer"""
        if self.get_trainer_by_id(trainer_id) is None:
            raise UserNotFoundError("Trainer ID does not exist.")

        trainees = []
        found_trainees = self.mongo.db.trainee.find({
            "trainers": ObjectId(trainer_id)
        })

        if found_trainees is not None:
            for trainee in found_trainees:
                trainees.append(self.trainee_dict_to_class(trainee))

        return trainees

    def add_trainer(self, trainer: Trainer):
        """Adds a trainer to the database based on a provided trainer class."""
        if (self.get_trainer_by_username(trainer.username) is not None):
            raise UsernameTakenError("Username was taken.")

        if (self.get_trainee_by_username(trainer.username) is not None):
            raise UsernameTakenError("Username was taken.")

        trainer_dict = trainer.as_dict()
        trainer_dict.pop('_id', None)
        trainer_dict['password'] = password_sha256(trainer.password)
        self.mongo.db.trainer.insert_one(trainer_dict)

    def remove_trainer(self, id: str):
        """Deletes a trainer by trainer id."""
        self.mongo.db.trainer.delete_one({"_id": ObjectId(id)})

    """Workout Functions"""

    def workout_dict_to_class(self, workout_dict: Workout):
        """Takes in a workout dictionary and returns a Workout class"""
        workout_dict['_id'] = str(workout_dict['_id'])
        return Workout(**workout_dict)

    def get_workout_class_by_id(self, id: str):
        """Returns the Workout class found by the workout's id."""
        found_workout = self.mongo.db.workout.find_one({"_id": ObjectId(id)})
        if found_workout:
            return self.workout_dict_to_class(found_workout)
        return None

    def get_workout_class_by_name(self, name: str):
        """Returns the Workout class found by the workout's name."""
        found_workout = self.mongo.db.workout.find_one({"name": name})
        if found_workout:
            return self.workout_dict_to_class(found_workout)
        return None

    def set_workout_creator_id(self, id: str, creator_id: str):
        """Updates a workout's creator id given a workout id."""
        self.mongo.db.workout.update_one(
            {"_id": ObjectId(id)},
            {
                "$set": {
                    "creator_id": creator_id
                }
            })

    def set_workout_name(self, id: str, name: str):
        """Updates a workout's name given a workout id."""
        self.mongo.db.workout.update_one(
            {"_id": ObjectId(id)},
            {
                "$set": {
                    "name": name
                }
            })

    def set_workout_difficulty(self, id: str, difficulty: str):
        """Updates a workout's difficulty given a workout id."""
        self.mongo.db.workout.update_one(
            {"_id": ObjectId(id)},
            {
                "$set": {
                    "difficulty": difficulty
                }
            })

    def set_workout_about(self, id: str, about: str):
        """Updates a workout's about information given a workout id."""
        self.mongo.db.workout.update_one(
            {"_id": ObjectId(id)},
            {
                "$set": {
                    "about": about
                }
            })

    def set_workout_exp(self, id: str, exp: str):
        """Updates a workout's experience points given a workout id."""
        self.mongo.db.workout.update_one(
            {"_id": ObjectId(id)},
            {
                "$set": {
                    "exp": exp
                }
            })

    def remove_workout(self, id: str):
        """Deletes a workout by workout id."""
        self.mongo.db.workout.delete_one({"_id": ObjectId(id)})

    def add_workout(self, workout: Workout):
        """Adds a workout to the database based on a provided Workout class."""
        if self.get_trainee_by_id(workout.creator_id) is None or not self.get_trainer_by_id(workout.creator_id) is None:
            raise WorkoutCreatorIdNotFoundError("Creator Id Not Found")
        self.mongo.db.workout.insert_one({
            "creator_id": workout.creator_id,
            'name': workout.name,
            "difficulty": workout.difficulty,
            "about": workout.about,
            "exp": workout.exp})


class UsernameTakenError(ValueError):
    """If a username was taken within the database class"""
    pass


class UserNotFoundError(ValueError):
    """If a username was taken within the database class"""
    pass


class WorkoutCreatorIdNotFoundError(AttributeError):
    """Error for when Workout creator id is missing"""
    pass


class InvalidCharactersException(Exception):
    """Error for invalid user input"""
    pass
