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
                 exp: int = 0,
                 goal_weight: str = None,
                 goal_body_fat: str = None,
                 lng: float = 0,
                 lat: float = 0):
        """Constructor for Trainee class."""
        
        self._id = str(_id)
        self.username = str(username)
        self.password = str(password)
        self.name = str(name)
        self.phone = str(phone)
        self.body_type = str(body_type)
        self.body_fat = str(body_fat)
        self.height = str(height)
        self.weight = str(weight)
        self.exp = int(exp) if exp is not None else 0
        self.goal_weight = str(goal_weight)
        self.goal_body_fat = str(goal_body_fat)
        self.lng = lng
        self.lat = lat

    def as_dict(self):
        """Returns all attributes of the Trainee class as a dictionary."""
        return dict(self.__dict__)

    def __repr__(self):
        return f'User({self._id}, {self.username}, {self.password}, {self.name}, {self.phone}, {self.body_type}, {self.body_fat}, {self.height}, {self.weight}, {self.exp}, {self.goal_weight}, {self.goal_body_fat}, {self.lng}, {self.lat})'
