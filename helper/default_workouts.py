from pymongo import MongoClient
client = MongoClient('mongodb://localhost:27017')

defaultWorkouts = [
  {"_id": 0, "creator_id": 0, "name": "curls", "difficulty": "easy", "about": "biceps", "exp": 1000, "is_complete": False},
  {"_id": 1, "creator_id": 1, "name": "russian twists", "difficulty": "medium", "about": "abs", "exp": 2000, "is_complete": False},
  {"_id": 2, "creator_id": 2, "name": "burpees", "difficulty": "hard", "about": "stamina", "exp": 3000, "is_complete": False},
  {"_id": 3, "creator_id": 3, "name": "20lb plate pullups", "difficulty": "insane", "about": "lats, biceps, deltoids", "exp": 5000, "is_complete": False}
]

db = client.flaskDatabase
db.workout.insert_many(defaultWorkouts)
