class User:
    def __init__(self,
                 _id: str,
                 username: str,
                 password: str,
                 name: str = None,
                 phone: int = None,
                 body_type: str = None,
                 body_fat: str = None,
                 height: str = None,
                 weight: str = None,
                 exp: str = None,
                 goal_weight: str = None,
                 goal_body_fat: str = None,
                 lng: float = None,
                 lat: float = None):
        """Constructor for Trainee class."""

        self._id = _id
        self.username = username
        self.password = password
        self.name = name
        self.phone = phone
        self.body_type = body_type
        self.body_fat = body_fat
        self.height = height
        self.weight = weight
        self.exp = exp
        self.goal_weight = goal_weight
        self.goal_body_fat = goal_body_fat
        self.lng = lng
        self.lat = lat

    def as_dict(self):
        """Returns all attributes of the Trainee class as a dictionary."""
        return dict(self.__dict__)

    def __repr__(self):
        return f'User({self._id}, {self.username}, {self.password}, {self.name}, {self.phone}, {self.body_type}, {self.body_fat}, {self.height}, {self.weight}, {self.exp}, {self.goal_weight}, {self.goal_body_fat}, {self.lng}, {self.lat})'
