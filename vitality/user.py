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
        self.__dict__.update(dict(
            _id=_id,
            username=username,
            password=password,
            name=name,
            location=location,
            phone=phone,
            body_type=body_type,
            body_fat=body_fat,
            height=height,
            weight=weight,
            exp=exp,
            goal_weight=goal_weight,
            goal_body_fat=goal_body_fat
        ))

    def as_dict(self):
        """Returns all attributes of the Trainee class as a dictionary."""
        return self.__dict__
