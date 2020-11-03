class User:
    def __init__(self, id: str, username: str, password: str, name: str = None, location: str = None, phone: int = None):
        """Constructor for Trainee class."""
        self.__dict__.update(dict(
            id=id,
            username=username,
            password=password,
            name=name,
            location=location,
            phone=phone
        ))

    def as_dict(self):
        """Returns all attributes of the Trainee class as a dictionary."""
        return self.__dict__
