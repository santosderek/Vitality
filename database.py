from flask_pymongo import PyMongo


class Database:
    def __init__(self, app):
        self.mongo = PyMongo(app)

    def set_username(self, id, username):
        self.mongo.db.user.update_one({"id": id}, {"$set": {
            "username": username
        }
        })

    def get_username(self, id, username):
        return self.mongo.db.user.find_one({"id": id, "username": username})

    def set_password(self, id, password):
        self.mongo.db.user.update_one({"id": id}, {"$set": {
            "password": password
        }
        })

    def get_password(self, id, password):
        return self.mongo.db.user.find_one({"id": id, "password": password})

    def set_location(self, id, location):
        self.mongo.db.user.update_one({"id": id}, {"$set": {
            "location": location
        }
        })

    def get_location(self, id, location):
        return self.mongo.db.user.find_one({"id": id, "location": location})

    def set_phone(self, id, phone):
        self.mongo.db.user.update_one({"id": id}, {"$set": {
            "phone": phone
        }
        })

    def get_phone(self, id, phone):
        return self.mongo.db.user.find_one({"id": id, "phone": phone})

    def check_id(self, id):
        if self.mongo.db.user.find_one({"id": id}):
            print("Error! ID is taken.")
        else:
            print("ID is free")

    def add_user(self, user):
        self.set_username(user.id, user.username)
        self.set_password(user.id, user.password)
        self.set_location(user.id, user.location)
        self.set_phone(user.id, user.phone)
