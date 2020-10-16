from flask_pymongo import PyMongo

class Database():
    def __init__(self, app):
        self.mongo = PyMongo(app)

    def set_username(self, id, username):
        self.mongo.db.user.insert_One({"username": username})

    def get_username(self, id, username):
        return self.mongo.db.user.findOne({"username": username})

    def set_password(self, id, password):
        self.mongo.db.user.insert_One({"password": password})

    def get_password(self, id, password):
        return self.mongo.db.user.findOne({"password": password})

    def set_location(self, id, location):
        self.mongo.db.user.insert_One({"location": location})

    def get_location(self, id, location):
        return self.mongo.db.user.findOne({"location": location})

    def set_phone(self, id, phone):
        self.mongo.db.user.insert_One({"phone": phone})

    def get_phone(self, id, phone):
        return self.mongo.db.user.findOne({"phone": phone})

    def add_user(self, user):
        self.set_username(user.id, user.username)
        self.set_password(user.id, user.password)
        self.set_location(user.id, user.location)
        self.set_phone(user.id, user.phone)


