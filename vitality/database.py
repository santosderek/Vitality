from flask_pymongo import PyMongo
from user import User 

class Database:
    def __init__(self, app):
        self.mongo = PyMongo(app)

    def get_user_class_by_id(self, id):
        found_user = self.mongo.db.user.find_one({"id": id})
        user = User(
            id        = found_user['id'],
            username  = found_user['username'],
            password  = found_user['password'],
            firstname = found_user['firstname'],
            lastname  = found_user['lastname'],
            location  = found_user['location'],
            phone     = found_user['phone']
        )
        return user

    def get_by_id(self, id):
        return self.mongo.db.user.find_one({"id": id})
    

    def get_by_username(self, username):
        return self.mongo.db.user.find_one({"username": username})


    def set_username(self, id, username):
        self.mongo.db.user.update_one({"id": id}, {"$set": {
            "username": username
        }
        })

    def set_password(self, id, password):
        self.mongo.db.user.update_one({"id": id}, {"$set": {
            "password": password
        }
        })

    def set_location(self, id, location):
        self.mongo.db.user.update_one({"id": id}, {"$set": {
            "location": location
        }
        })

    def set_phone(self, id, phone):
        self.mongo.db.user.update_one({"id": id}, {"$set": {
            "phone": phone
        }
        })

    def remove_user(self, id): 
        self.mongo.db.user.delete_one({'id': id})

    def check_id(self, id):
        if self.mongo.db.user.find_one({"id": id}):
            return False
        else:
            return True

    def add_user(self, user):
        self.mongo.db.user.insert_one({
            'id':user.id, 
            'username': user.username, 
            'password': user.password, 
            'firstname': user.firstname, 
            'lastname': user.lastname, 
            'location': user.location, 
            'phone': user.phone})



