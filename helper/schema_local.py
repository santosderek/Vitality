from pymongo import MongoClient
from vitality.configuration import Configuration

url = Configuration(path='vitality/configuration.json')
client = MongoClient(url.get_local_uri())

user = {
 "username": "admin",
 "password": "password",
 "workouts": "arms",
 "location": "USA",
 "experience": 0
 }

workout = {
 "w_name": "curls",
 "difficulty": "easy",
 "id": 0,
 "about": "biceps",
 "exp_rewards": 10
}

trainer = {
 "t_name": "bob",
 "t_location": "1234 Road",
 "t_time": "12:00",
 "t_focus": "arms"
 }

db = client.admin_user
db.user.insert_one(user)
db.workout.insert_one(workout)
db.trainer.insert_one(trainer)

