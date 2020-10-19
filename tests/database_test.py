from flask import Flask
from flask_pymongo import PyMongo
from vitality.database import Database
from vitality.user import User

app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb://localhost:27017/flaskDatabase"
mongo = PyMongo(app)


def test_set_username():
    database = Database(app)
    new_user = User(1, username="derek", password="derek")
    database.add_user(new_user)

    db_get = database.get_username(new_user.id, new_user.username)
    db_get.pop('_id')
    print(db_get)
    assert db_get == {"id": new_user.id, "username": new_user.username, "password": new_user.password, "location": new_user.location, "phone": new_user.phone}

    new_user.username = "elijah"
    database.set_username(new_user.id, new_user.username)

    db_get_2 = database.get_username(new_user.id, new_user.username)
    db_get_2.pop('_id')
    print(db_get_2)
    assert db_get_2 == {"id": new_user.id, "username": new_user.username,  "password": new_user.password, "location": new_user.location, "phone": new_user.phone}

    database.check_id(new_user.id)


test_set_username()
