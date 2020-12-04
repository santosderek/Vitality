import datetime
class Event:
    def __init__(self, _id: str, creator_id: str, date: datetime, title: str, description: str,):
        """Constructor for Workout class."""
        self._id = _id
        self.creator_id = creator_id
        self.date = date
        self.title = title
        self.description = description

    def as_dict(self):
        """Returns all attributes of the Workout class as a dictionary."""
        return dict(self.__dict__)

    def __repr__(self):
        return f'Event({self._id}, {self.creator_id}, {self.date}, {self.title}, {self.description})'
