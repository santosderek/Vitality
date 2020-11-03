class Workout:
    def __init__(self, _id: str, creator_id: str, name: str, difficulty: str = "easy", about: str = None, exp: int = None):
        """Constructor for Workout class."""
        self.__dict__.update(dict(
            _id=_id,
            creator_id=creator_id,
            name=name,
            difficulty=difficulty,
            about=about,
            exp=exp
        ))

    def as_dict(self):
        """Returns all attributes of the Workout class as a dictionary."""
        return self.__dict__
