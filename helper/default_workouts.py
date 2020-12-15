from pymongo import MongoClient
client = MongoClient('mongodb://localhost:27017')

defaultWorkouts = [
  {"_id": 0, "creator_id": 0, "name": "curls", "difficulty": "easy", "about": "biceps", "is_complete": False},
  {"_id": 1, "creator_id": 1, "name": "russian twists", "difficulty": "medium", "about": "abs", "is_complete": False},
  {"_id": 2, "creator_id": 2, "name": "burpees", "difficulty": "hard", "about": "stamina", "is_complete": False},
  {"_id": 3, "creator_id": 3, "name": "20lb plate pullups", "difficulty": "insane", "about": "lats, biceps, deltoids", "is_complete": False}
]

db = client.flaskDatabase
db.workout.insert_many(defaultWorkouts)
