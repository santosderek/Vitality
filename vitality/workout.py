class Workout:
    def __init__(self, id: str, creator_id: str, name: str, difficulty: str = "easy", about: str = None, exp: int = None):
        """Constructor for Workout class."""
        self.id = id
        self.creator_id = creator_id
        self.name = name
        self.difficulty = difficulty
        self.about = about
        self.exp = exp

    def as_dict(self):
        """Returns all attributes of the Workout class as a dictionary."""
        return {
            "_id": self.id,
            "creator_id": self.creator_id,
            "name": self.name,
            "difficulty": self.difficulty,
            "about": self.about,
            "exp": self.exp,
        }
