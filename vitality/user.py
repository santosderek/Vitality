class User:
    def __init__(self,
                 _id: str,
                 username: str,
                 password: str,
                 name: str = None,
                 location: str = None,
                 phone: int = None,
                 body_type: str = None,
                 body_fat: str = None,
                 height: str = None,
                 weight: str = None,
                 exp: str = None,
                 goal_weight: str = None,
                 goal_body_fat: str = None):
        """Constructor for Trainee class."""

        self._id = _id
        self.username = username
        self.password = password
        self.name = name
        self.location = location
        self.phone = phone
        self.body_type = body_type
        self.body_fat = body_fat
        self.height = height
        self.weight = weight
        self.exp = exp
        self.goal_weight = goal_weight
        self.goal_body_fat = goal_body_fat

    def as_dict(self):
        """Returns all attributes of the Trainee class as a dictionary."""
        return dict(self.__dict__)
