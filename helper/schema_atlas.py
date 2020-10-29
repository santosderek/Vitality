from pymongo import MongoClient
from vitality.configuration import Configuration

url = Configuration(path='vitality/configuration.json')
cluster = MongoClient(url.get_atlas_uri())

user = {
 "username": "admin",
 "password": "password",
 "workouts": "arms",
 "location": "USA",
 "experience": 0
 }

workout = {
 "name": "curls",
 "difficulty": "easy",
 "id": 0,
 "about": "biceps",
 "exp": 10
}

trainer = {
 "t_name": "bob",
 "t_location": "1234 Road",
 "t_time": "12:00",
 "t_focus": "arms"
 }

db = cluster["admin_user"]
collection_user = db["user"]
collection_workout = db["workout"]
collection_trainer = db["trainer"]
collection_user.insert_one(user)
collection_workout.insert_one(workout)
collection_trainer.insert_one(trainer)

