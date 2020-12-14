DEFAULT_EASY_EXP = 1000
DEFAULT_MEDIUM_EXP = 2000
DEFAULT_HARD_EXP = 3000
DEFAULT_INSANE_EXP = 5000


class Workout:
    def __init__(self, _id: str, creator_id: str, name: str, difficulty: str = "novice", about: str = None, is_complete: bool = False):
        """Constructor for Workout class."""
        self._id = _id
        self.creator_id = creator_id
        self.name = name
        self.difficulty = difficulty
        self.about = about
        self.is_complete = is_complete

    def __repr__(self):
        """Returns all attributes of the Workout class as a dictionary."""
        return f'Workout({self._id}, {self.creator_id}, {self.name}, {self.difficulty}, {self.about}, {self.is_complete})'

    def as_dict(self):
        """Returns all attributes of the Workout class as a dictionary."""
        return dict(self.__dict__)
