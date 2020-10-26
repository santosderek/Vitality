from flask_pymongo import PyMongo
from .user import User
from .workout import Workout
from bson.objectid import ObjectId

class Database:
    def __init__(self, app):
        """Constructor for Database class.""" 
        self.mongo = PyMongo(app)

    def get_user_class_by_id(self, id):
        """Returns the User class of the User found by the user's id."""
        found_user = self.mongo.db.user.find_one({"_id": ObjectId(id)})

        if found_user: 
            user = User(
                id        = str(found_user['_id']),
                username  = found_user['username'],
                password  = found_user['password'],
                firstname = found_user['firstname'],
                lastname  = found_user['lastname'],
                location  = found_user['location'],
                phone     = found_user['phone']
            )
            return user
        return None

    def get_user_class_by_username(self, username):
        """Returns the User class of the User found by the user's username."""
        found_user = self.mongo.db.user.find_one({"username": username})

        if found_user: 
            user = User(
                id        = str(found_user['_id']),
                username  = found_user['username'],
                password  = found_user['password'],
                firstname = found_user['firstname'],
                lastname  = found_user['lastname'],
                location  = found_user['location'],
                phone     = found_user['phone']
            )
            return user
        return None

    def get_workout_class_by_id(self, id):
        """Returns the Workout class found by the workout's id."""
        found_workout = self.mongo.db.workout.find_one({"_id": ObjectId(id)})

        if found_workout:
            workout = Workout(
                id         = str(found_workout['_id']),
                creator_id = found_workout['creator_id'],
                name = found_workout['name'],
                difficulty = found_workout['difficulty'],
                about = found_workout['about'],
                exp_rewards = found_workout['exp_rewards']
            )
            return workout
        return None


    def get_workout_class_by_name(self, name):
        """Returns the Workout class found by the workout's name."""
        found_workout = self.mongo.db.workout.find_one({"name": name})

        if found_workout:
            workout = Workout(
                id         = str(found_workout['_id']),
                creator_id = found_workout['creator_id'],
                name = found_workout['name'],
                difficulty = found_workout['difficulty'],
                about = found_workout['about'],
                exp_rewards = found_workout['exp_rewards']
            )
            return workout
        return None

    def get_by_id(self, id):
        """Returns the User class found by the user's id."""
        return self.mongo.db.user.find_one({"_id": ObjectId(id)})
    

    def get_by_username(self, username):
        """Returns the User class found by the user's username."""
        return self.mongo.db.user.find_one({"username": username})


    def set_username(self, id, username):
        """Updates a user's username given a user id."""
        self.mongo.db.user.update_one({"_id": ObjectId(id)}, {"$set": {
            "username": username
        }
        })

    def set_password(self, id, password):
        """Updates a user's password given a user id."""
        self.mongo.db.user.update_one({"_id": ObjectId(id)}, {"$set": {
            "password": password
        }
        })

    def set_location(self, id, location):
        """Updates a user's location given a user id."""
        self.mongo.db.user.update_one({"_id": ObjectId(id)}, {"$set": {
            "location": location
        }
        })

    def set_phone(self, id, phone):
        """Updates a user's phone number given a user id."""
        self.mongo.db.user.update_one({"_id": ObjectId(id)}, {"$set": {
            "phone": phone
        }
        })

    def set_firstname(self, id, firstname):
        """Updates a user's firstname given a user id."""
        self.mongo.db.user.update_one({"_id": ObjectId(id)}, {"$set": {
            "firstname": firstname
        }
        })

    def set_lastname(self, id, lastname):
        """Updates a user's lastname given a user id."""
        self.mongo.db.user.update_one({"_id": ObjectId(id)}, {"$set": {
            "lastname": lastname
        }
        })

    def set_workout_creator_id(self, id, creator_id):
        """Updates a workout's creator id given a workout id."""
        self.mongo.db.workout.update_one({"_id": ObjectId(id)}, {"$set": {
            "creator_id": creator_id
        }
        })

    def set_workout_name(self, id, name):
        """Updates a workout's name given a workout id."""
        self.mongo.db.workout.update_one({"_id": ObjectId(id)}, {"$set": {
            "name": name
        }
        })

    def set_workout_difficulty(self, id, difficulty):
        """Updates a workout's difficulty given a workout id."""
        self.mongo.db.workout.update_one({"_id": ObjectId(id)}, {"$set": {
            "difficulty": difficulty
        }
        })

    def set_workout_id(self, id, local_id):
        """Updates a workout's id given a workout id."""
        self.mongo.db.workout.update_one({"_id": ObjectId(id)}, {"$set": {
            "id": local_id
        }
        })

    def set_workout_about(self, id, about):
        """Updates a workout's about information given a workout id."""
        self.mongo.db.workout.update_one({"_id": ObjectId(id)}, {"$set": {
            "about": about
        }
        })

    def set_workout_exp(self, id, exp):
        """Updates a workout's experience points given a workout id."""
        self.mongo.db.workout.update_one({"_id": ObjectId(id)}, {"$set": {
            "exp_rewards": exp
        }
        })


    def remove_user(self, id): 
        """Deletes a user by user id."""
        self.mongo.db.user.delete_one({"_id": ObjectId(id)})

    def remove_workout(self, id):
        """Deletes a workout by workout id."""
        self.mongo.db.workout.delete_one({"_id": ObjectId(id)})

    def check_id(self, id):
        """Returns true of false if the user is found by user id."""
        if self.mongo.db.user.find_one({"_id": ObjectId(id)}):
            return False
        else:
            return True

    def check_workout_id(self, id):
        """Returns true of false if the workout is found by workout id."""
        if self.mongo.db.workout.find_one({"_id": ObjectId(id)}):
            return False
        else:
            return True

    def check_workout_creator_id(self, id):
        """Returns true of false if the workout is found by creator id."""
        if self.mongo.db.workout.find_one({"creator_id": id}):
            return False
        else:
            return True

    def add_user(self, user):
        """Adds a user to the database based on a provided User class."""
        self.mongo.db.user.insert_one({
            'username': user.username, 
            'password': user.password, 
            'firstname': user.firstname, 
            'lastname': user.lastname, 
            'location': user.location, 
            'phone': user.phone})

    def add_workout(self, workout):
        """Adds a workout to the database based on a provided Workout class."""
        self.mongo.db.workout.insert_one({
            "creator_id": workout.creator_id,
            'name': workout.name,
            "difficulty": workout.difficulty,
            "about": workout.about,
            "exp_rewards": workout.exp_rewards})
