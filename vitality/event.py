from datetime import datetime
class Event:
    def __init__(self, _id: str, creator_id: str, date: datetime, title: str, description: str, participant_id: str):
        """Constructor for Workout class."""
        self._id = _id
        self.creator_id = creator_id
        self.title = title
        self.description = description
        self.participant_id = participant_id

        if type(date) is datetime:
            self.date = date
        else:
            self.date = datetime(*date)

    def as_dict(self):
        """
        Returns all attributes of the Workout class as a dictionary.
        {
            '_id': str,
            'creator_id': str,
            'title': str,
            'description': str,
            'date': str
        }
        """
        return_dict = dict(self.__dict__)
        return_dict['date'] = str(return_dict['date'])
        return return_dict

    def __repr__(self):
        return f'Event({self._id}, {self.creator_id}, {self.date}, {self.title}, {self.description}, {self.participant_id})'
