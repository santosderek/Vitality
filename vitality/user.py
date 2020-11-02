class User:
    def __init__(self, values_dict: dict):
        """Constructor for Trainee class."""
        self.__dict__.update(values_dict)

    def as_dict(self):
        """Returns all attributes of the Trainee class as a dictionary."""
        return self.__dict__
