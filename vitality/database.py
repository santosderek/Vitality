from .invitation import Invitation
from .trainee import Trainee
from .trainer import Trainer
from .workout import Workout
from .event import Event
from bson.objectid import ObjectId
from pymongo import MongoClient
from markupsafe import escape
import re
import hashlib

from vitality import workout


def password_sha256(password: str):
    return hashlib.sha256(escape(password).encode()).hexdigest()


class Database:
    def __init__(self, uri):
        """Constructor for Database class."""
        self.mongo = MongoClient(uri)['flaskDatabase']

    """ Trainee Functions """

    def trainee_dict_to_class(self, trainee_dict: dict):
        """Return a Trainee class from a dictionary"""
        trainee_dict['_id'] = str(trainee_dict['_id'])
        trainee_dict['trainers'] = [str(trainer_id)
                                    for trainer_id in trainee_dict['trainers']]
        # WARNING: Removed converting trainers to classes due to unintended recursion
        return Trainee(**trainee_dict)

    def get_trainee_id_by_login(self, username: str, password: str):
        """
        Return the trainer id if login matches.

        username: str - The user created user name.
        password: str - The user created password hashed in SHA256. 
        """
        trainee = self.mongo.trainee.find_one({
            'username': username,
            'password': password})

        return str(trainee['_id']) if trainee is not None else None

    def get_trainee_by_id(self, id: str):
        """Returns the Trainee class of the User found by the trainee's id."""
        found_user = self.mongo.trainee.find_one({"_id": ObjectId(id)})

        if found_user:
            return self.trainee_dict_to_class(found_user)

        return None

    def get_trainee_by_username(self, username: str):
        """Returns the Trainee class of the User found by the trainee's username."""
        found_user = self.mongo.trainee.find_one({"username": username})

        if found_user:
            return self.trainee_dict_to_class(found_user)

        return None

    def set_trainee_username(self, id: str, username: str):
        """Updates a trainee's username given a user id."""
        self.mongo.trainee.update_one(
            {"_id": ObjectId(id)},
            {
                "$set": {
                    "username": username
                }
            })

    def set_trainee_password(self, id: str, password: str):
        """Updates a trainee's password given a user id."""
        self.mongo.trainee.update_one(
            {"_id": ObjectId(id)},
            {
                "$set": {
                    "password": password_sha256(password)
                }
            })

    def set_trainee_location(self, id: str, location: str):
        """Updates a trainee's location given a user id."""
        self.mongo.trainee.update_one(
            {"_id": ObjectId(id)},
            {
                "$set": {
                    "location": location
                }
            })

    def set_trainee_phone(self, id: str, phone: int):
        """Updates a trainee's phone number given a user id."""
        self.mongo.trainee.update_one(
            {"_id": ObjectId(id)},
            {
                "$set": {
                    "phone": phone
                }
            })

    def set_trainee_name(self, id: str, name: str):
        """Updates a trainee's name given a user id."""
        self.mongo.trainee.update_one(
            {"_id": ObjectId(id)},
            {
                "$set": {
                    "name": name
                }
            })

    def trainee_add_trainer(self, trainee_id: str, trainer_id: str):
        """Add trainer object id to trainee's trainer list"""
        if self.get_trainee_by_id(trainee_id) is None or self.get_trainee_by_id(trainee_id) is None:
            raise UserNotFoundError("Trainee ID does not exist.")

        if self.get_trainer_by_id(trainer_id) is None or self.get_trainer_by_id(trainer_id) is None:
            raise UserNotFoundError("Trainer ID does not exist.")

        self.mongo.trainee.update_one(
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
        self.mongo.trainee.insert_one(trainee_dict)

    def add_trainee_experience(self, trainee_id: str, value: int):

        self.mongo.trainee.update_one(
            {
                '_id': ObjectId(trainee_id)
            },
            {
                '$inc': {
                    'exp': int(value)
                }
            }
        )

    def remove_trainee(self, id: str):
        """Deletes a trainee by trainee id."""
        self.mongo.trainee.delete_one({"_id": ObjectId(id)})

        # Remove trainee from trainer's list
        self.mongo.trainer.update_many(
            {},
            {
                "$pull": {
                    "trainees": {
                        "$in": [ObjectId(id)]
                    }
                }
            }

        )

    def trainee_remove_trainer(self, trainee_id: str, trainer_id: str):
        """Remove trainer object id from trainees's trainer list"""
        if self.get_trainee_by_id(trainee_id) is None or self.get_trainee_by_id(trainee_id) is None:
            raise UserNotFoundError("Trainee ID does not exist.")

        if self.get_trainer_by_id(trainer_id) is None or self.get_trainer_by_id(trainer_id) is None:
            raise UserNotFoundError("Trainer ID does not exist.")

        self.mongo.trainee.update_one(
            {
                '_id': ObjectId(trainee_id)
            },
            {
                "$pull": {
                    "trainers": {
                        "$in": [ObjectId(trainer_id)]
                    }
                }
            }
        )

    """ Trainer Functions """

    def trainer_dict_to_class(self, trainer_dict: str):
        """Return a Trainer class from a dictionary"""
        trainer_dict['_id'] = str(trainer_dict['_id'])
        trainer_dict['trainees'] = [str(trainee_id)
                                    for trainee_id in trainer_dict['trainees']]
        # WARNING: Removed converting trainees to classes due to unintended recursion
        return Trainer(**trainer_dict)

    def get_trainer_id_by_login(self, username: str, password: str):
        """Return the trainer id if login matches"""
        trainer = self.mongo.trainer.find_one({
            'username': username,
            'password': password})

        return str(trainer['_id']) if trainer is not None else None

    def get_trainer_by_username(self, username: str):
        """Returns the trainer class of the trainer found by the trainer's username."""
        found_user = self.mongo.trainer.find_one(
            {"username": escape(username)})
        if found_user:
            return self.trainer_dict_to_class(found_user)

        return None

    def get_trainer_by_id(self, id: str):
        """Returns the trainer class of the trainer found by the trainer's id."""
        found_trainer = self.mongo.trainer.find_one({"_id": ObjectId(id)})
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

        found_trainers = self.mongo.trainer.find(
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
        found_trainees = self.mongo.trainee.find(
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
        self.mongo.trainer.update_one(
            {"_id": ObjectId(id)},
            {
                "$set": {
                    "username": username
                }
            })

    def set_trainer_password(self, id: str, password: str):
        """Updates a trainer's password given a trainer id."""
        self.mongo.trainer.update_one(
            {"_id": ObjectId(id)},
            {
                "$set": {
                    "password": password_sha256(password)
                }
            })

    def set_trainer_location(self, id: str, location: str):
        """Updates a trainer's location given a trainer id."""
        self.mongo.trainer.update_one(
            {"_id": ObjectId(id)},
            {
                "$set": {
                    "location": location
                }
            })

    def set_trainer_phone(self, id: str, phone: str):
        """Updates a trainer's phone number given a trainer id."""
        self.mongo.trainer.update_one(
            {"_id": ObjectId(id)},
            {
                "$set": {
                    "phone": phone
                }
            })

    def set_trainer_name(self, id: str, name: str):
        """Updates a trainer's name given a trainer id."""
        self.mongo.trainer.update_one(
            {"_id": ObjectId(id)},
            {
                "$set": {
                    "name": name
                }
            })

    def trainer_add_trainee(self, trainer_id: str, trainee_id: str):
        """Add trainer object id to trainee's trainer list"""
        if self.get_trainee_by_id(trainee_id) is None or self.get_trainee_by_id(trainee_id) is None:
            raise UserNotFoundError("Trainee ID does not exist.")

        if self.get_trainer_by_id(trainer_id) is None or self.get_trainer_by_id(trainer_id) is None:
            raise UserNotFoundError("Trainer ID does not exist.")

        self.mongo.trainer.update_one(
            {"_id": ObjectId(trainer_id)},
            {
                "$addToSet": {
                    "trainees": ObjectId(trainee_id)
                }
            })

    def trainer_remove_trainee(self, trainer_id: str, trainee_id: str):
        """Remove trainee object id from trainers's trainee list"""
        if self.get_trainee_by_id(trainee_id) is None or self.get_trainee_by_id(trainee_id) is None:
            raise UserNotFoundError("Trainee ID does not exist.")

        if self.get_trainer_by_id(trainer_id) is None or self.get_trainer_by_id(trainer_id) is None:
            raise UserNotFoundError("Trainer ID does not exist.")

        self.mongo.trainer.update_one(
            {
                '_id': ObjectId(trainer_id)
            },
            {
                "$pull": {
                    "trainees": {
                        "$in": [ObjectId(trainee_id)]
                    }
                }
            }
        )

    def add_trainer(self, trainer: Trainer):
        """Adds a trainer to the database based on a provided trainer class."""
        if (self.get_trainer_by_username(trainer.username) is not None):
            raise UsernameTakenError("Username was taken.")

        if (self.get_trainee_by_username(trainer.username) is not None):
            raise UsernameTakenError("Username was taken.")

        trainer_dict = trainer.as_dict()
        trainer_dict.pop('_id', None)
        trainer_dict['password'] = password_sha256(trainer.password)
        self.mongo.trainer.insert_one(trainer_dict)

    def add_trainer_experience(self, trainer_id: str, value: int):

        self.mongo.trainer.update_one(
            {
                '_id': ObjectId(trainer_id)
            },
            {
                '$inc': {
                    'exp': int(value)
                }
            }
        )

    def remove_trainer(self, id: str):
        """Deletes a trainer by trainer id."""
        self.mongo.trainer.delete_one({"_id": ObjectId(id)})

        # Remove trainer from trainee's list
        self.mongo.trainee.update_many(
            {},
            {
                "$pull": {
                    "trainers": {
                        "$in": [ObjectId(id)]
                    }
                }
            }
        )

    """Workout Functions"""

    def workout_dict_to_class(self, workout_dict: Workout):
        """Takes in a workout dictionary and returns a Workout class"""
        workout_dict['_id'] = str(workout_dict['_id'])
        workout_dict['creator_id'] = str(workout_dict['creator_id'])
        return Workout(**workout_dict)

    def get_workout_by_id(self, id: str):
        """Returns the Workout class found by the workout's id."""
        found_workout = self.mongo.workout.find_one({"_id": ObjectId(id)})
        if found_workout:
            return self.workout_dict_to_class(found_workout)
        return None

    def get_workout_by_attributes(self, **kwargs):
        """
        Returns a single workout based on the keyword arguments passed to the function.
        Each key represents the attribute to append to the find function.
        If a workout with the passed key value pairs are not found, then we raise a WorkoutNotFound
        error. 
        """
        if 'creator_id' in kwargs:
            kwargs['creator_id'] = ObjectId(kwargs['creator_id'])
        if '_id' in kwargs:
            kwargs['_id'] = ObjectId(kwargs['_id'])

        found_workout = self.mongo.workout.find_one({**kwargs})
        if found_workout:
            return self.workout_dict_to_class(found_workout)
        else:
            raise WorkoutNotFound("Workout with key/value pairs not found.")

    def get_all_workouts_by_creatorid(self, creator_id: str):
        """Returns the Workout class found by the workout's id."""
        found_workouts = self.mongo.workout.find(
            {"creator_id": ObjectId(creator_id)})
        workouts = []
        if found_workouts:
            for workout in found_workouts:
                workouts.append(self.workout_dict_to_class(workout))
        return workouts

    def set_workout_creator_id(self, id: str, creator_id: str):
        """Updates a workout's creator id given a workout id."""
        self.mongo.workout.update_one(
            {"_id": ObjectId(id)},
            {
                "$set": {
                    "creator_id": ObjectId(creator_id)
                }
            })

    def set_workout_name(self, id: str, name: str):
        """Updates a workout's name given a workout id."""
        self.mongo.workout.update_one(
            {"_id": ObjectId(id)},
            {
                "$set": {
                    "name": name
                }
            })

    def set_workout_difficulty(self, id: str, difficulty: str):
        """Updates a workout's difficulty given a workout id."""
        self.mongo.workout.update_one(
            {"_id": ObjectId(id)},
            {
                "$set": {
                    "difficulty": difficulty
                }
            })

    def set_workout_about(self, id: str, about: str):
        """Updates a workout's about information given a workout id."""
        self.mongo.workout.update_one(
            {"_id": ObjectId(id)},
            {
                "$set": {
                    "about": about
                }
            })

    def set_workout_status(self, creator_id: str, name: str, is_complete: bool):
        self.mongo.workout.update_one(
            {
                'creator_id': ObjectId(creator_id),
                "name": name
            },
            {
                "$set": {
                    "is_complete": is_complete
                }
            })

    def remove_workout(self, id: str):
        """Deletes a workout by workout id."""
        self.mongo.workout.delete_one({"_id": ObjectId(id)})

    def add_workout(self, workout: Workout):
        """Adds a workout to the database based on a provided Workout class."""
        if self.get_trainee_by_id(workout.creator_id) is None and self.get_trainer_by_id(workout.creator_id) is None:
            raise WorkoutCreatorIdNotFoundError("Creator Id Not Found")
        self.mongo.workout.insert_one({
            "creator_id": ObjectId(workout.creator_id),
            'name': workout.name,
            "difficulty": workout.difficulty,
            "about": workout.about,
            "is_complete": workout.is_complete})

    """Invitation"""

    def create_invitation(self, sender: str, recipient: str):
        """
        Create an invitation based on a sender and recipient.
            sender: str - The id given to a user document by mongodb.
            recipient: str - The id given to a user document by mongodb.

            returns the object id of the invitation.
        """
        if self.get_trainee_by_id(sender) is None and self.get_trainer_by_id(sender) is None:
            raise UserNotFoundError('Sender could not be found')
        if self.get_trainee_by_id(recipient) is None and self.get_trainer_by_id(recipient) is None:
            raise UserNotFoundError('Recipient could not be found')
        invitation = self.mongo.invitation.insert_one({
            'sender': ObjectId(sender),
            'recipient': ObjectId(recipient)
        })
        return str(invitation.inserted_id)

    def delete_invitation(self, invitation_id: str):
        """
        Delete an invitation from the database
            invitation_id: str - The id given to the invitation document by mongodb.

        """
        self.mongo.invitation.delete_one({
            '_id': ObjectId(invitation_id)
        })

    def search_invitation(self, invitation_id: str):
        """
        Search for an invitation based on a user_id.
            invitation_id: str - The id given to the invitation document by mongodb.

            returns the document found. 
        """
        invitation = self.mongo.invitation.find_one({
            '_id': ObjectId(invitation_id)
        })

        if invitation is None:
            raise InvitationNotFound('Invitation not found')
        else:
            return Invitation(str(invitation['_id']), str(invitation['sender']), str(invitation['recipient']))

    def search_all_user_invitations(self, user_id: str):
        """
        Search for all invitations a user has sent and recieved.
            user_id: str - The id of the user given by mongodb.
        """
        database_sent = self.mongo.invitation.find({
            'sender': ObjectId(user_id)
        })
        database_recieved = self.mongo.invitation.find({
            'recipient': ObjectId(user_id)
        })

        all_sent = []
        all_recieved = []

        for item in database_sent:
            all_sent.append({
                '_id': str(item['_id']),
                'sender': str(item['sender']),
                'recipient': str(item['recipient']),
            })

        for item in database_recieved:
            all_recieved.append({
                '_id': str(item['_id']),
                'sender': str(item['sender']),
                'recipient': str(item['recipient']),
            })

        return (all_sent, all_recieved)

    def accept_invitation(self, invitation_id: str, accepter_id: str):
        """
        Removes the invitation and adds the trainee to trainer list and vice versa.
            invitation_id: str - The id of the invitation generated by mongodb.
            accepter_id: str - The id of the user that is accepting the id.
        """
        invitation = self.mongo.invitation.find_one({
            '_id': ObjectId(invitation_id),
            'recipient': ObjectId(accepter_id)
        })

        if invitation is None:
            raise InvitationNotFound(
                "Could not find a recipient with the given accepter id.")

        sender = self.get_trainee_by_id(invitation['sender']) or\
            self.get_trainer_by_id(invitation['sender'])
        recipient = self.get_trainee_by_id(invitation['recipient']) or\
            self.get_trainer_by_id(invitation['recipient'])

        if type(sender) is Trainer:
            self.trainer_add_trainee(sender._id, recipient._id)
            self.trainee_add_trainer(recipient._id, sender._id)

        elif type(sender) is Trainee:
            self.trainee_add_trainer(sender._id, recipient._id)
            self.trainer_add_trainee(recipient._id, sender._id)

        self.delete_invitation(invitation_id)

    def create_event(self, event: Event):
        """Creates an event document within the database using a passed Event class."""
        if event is None:
            raise EventNotFound("Event is None")

        event_dict = event.as_dict()
        event_dict.pop('_id')
        self.mongo.event.insert(**event_dict)

    def remove_event(self, event_id: str):
        """Removes an Event document based on the event document's id"""
        self.mongo.event.delete_one({
            '_id': ObjectId(event_id)
        })

    def list_events(self):
        pass


class EventNotFound(ValueError):
    """If a username was taken within the database class"""
    pass


class UsernameTakenError(ValueError):
    """If a username was taken within the database class"""
    pass


class UserNotFoundError(ValueError):
    """If a username was taken within the database class"""
    pass


class WorkoutNotFound(ValueError):
    """If a username was taken within the database class"""
    pass


class WorkoutCreatorIdNotFoundError(AttributeError):
    """Error for when Workout creator id is missing"""
    pass


class InvalidCharactersException(Exception):
    """Error for invalid user input"""
    pass


class InvitationNotFound(Exception):
    """Error for when an invitation is not found"""
    pass


class IncorrectRecipientID(Exception):
    """
    Error for when accepting an invitation. 
    The passed accepter's id must match the invitation's recipient id.
    """
    pass
