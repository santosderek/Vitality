from flask_pymongo import PyMongo
from .user import User 
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

    def remove_user(self, id): 
        self.mongo.db.user.delete_one({"_id": ObjectId(id)})

    def check_id(self, id):
        if self.mongo.db.user.find_one({"_id": ObjectId(id)}):
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



