from pymongo import MongoClient

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

cluster = MongoClient("mongodb+srv://laruffaelijah:4155_8675@cluster0.zq0eb.mongodb.net/admin_user?retryWrites=true&w=majority")
db = cluster["admin_user"]
collection_user = db["user"]
collection_workout = db["workout"]
collection_trainer = db["trainer"]
collection_user.insert_one(user)
collection_workout.insert_one(workout)
collection_trainer.insert_one(trainer)
