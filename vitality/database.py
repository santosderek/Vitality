from flask_pymongo import PyMongo
from .user import User
from .workout import Workout
from bson.objectid import ObjectId

class Database:
    def __init__(self, app):
        self.mongo = PyMongo(app)

    def get_user_class_by_id(self, id):
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
        return self.mongo.db.user.find_one({"_id": ObjectId(id)})
    

    def get_by_username(self, username):
        return self.mongo.db.user.find_one({"username": username})


    def set_username(self, id, username):
        self.mongo.db.user.update_one({"_id": ObjectId(id)}, {"$set": {
            "username": username
        }
        })

    def set_password(self, id, password):
        self.mongo.db.user.update_one({"_id": ObjectId(id)}, {"$set": {
            "password": password
        }
        })

    def set_location(self, id, location):
        self.mongo.db.user.update_one({"_id": ObjectId(id)}, {"$set": {
            "location": location
        }
        })

    def set_phone(self, id, phone):
        self.mongo.db.user.update_one({"_id": ObjectId(id)}, {"$set": {
            "phone": phone
        }
        })

    def set_firstname(self, id, firstname):
        self.mongo.db.user.update_one({"_id": ObjectId(id)}, {"$set": {
            "firstname": firstname
        }
        })

    def set_lastname(self, id, lastname):
        self.mongo.db.user.update_one({"_id": ObjectId(id)}, {"$set": {
            "lastname": lastname
        }
        })

    def set_workout_creator_id(self, id, creator_id):
        self.mongo.db.workout.update_one({"_id": ObjectId(id)}, {"$set": {
            "creator_id": creator_id
        }
        })

    def set_workout_name(self, id, name):
        self.mongo.db.workout.update_one({"_id": ObjectId(id)}, {"$set": {
            "name": name
        }
        })

    def set_workout_difficulty(self, id, difficulty):
        self.mongo.db.workout.update_one({"_id": ObjectId(id)}, {"$set": {
            "difficulty": difficulty
        }
        })

    def set_workout_id(self, id, local_id):
        self.mongo.db.workout.update_one({"_id": ObjectId(id)}, {"$set": {
            "id": local_id
        }
        })

    def set_workout_about(self, id, about):
        self.mongo.db.workout.update_one({"_id": ObjectId(id)}, {"$set": {
            "about": about
        }
        })

    def set_workout_exp(self, id, exp):
        self.mongo.db.workout.update_one({"_id": ObjectId(id)}, {"$set": {
            "exp_rewards": exp
        }
        })


    def remove_user(self, id): 
        self.mongo.db.user.delete_one({"_id": ObjectId(id)})

    def remove_workout(self, id):
        self.mongo.db.workout.delete_one({"_id": ObjectId(id)})

    def check_id(self, id):
        if self.mongo.db.user.find_one({"_id": ObjectId(id)}):
            return False
        else:
            return True

    def check_workout_id(self, id):
        if self.mongo.db.workout.find_one({"_id": ObjectId(id)}):
            return False
        else:
            return True

    def check_workout_creator_id(self, id):
        if self.mongo.db.workout.find_one({"creator_id": id}):
            return False
        else:
            return True

    def add_user(self, user):
        self.mongo.db.user.insert_one({
            'username': user.username, 
            'password': user.password, 
            'firstname': user.firstname, 
            'lastname': user.lastname, 
            'location': user.location, 
            'phone': user.phone})

    def add_workout(self, workout):
        self.mongo.db.workout.insert_one({
            "creator_id": workout.creator_id,
            'name': workout.name,
            "difficulty": workout.difficulty,
            "about": workout.about,
            "exp_rewards": workout.exp_rewards})
