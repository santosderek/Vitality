from .user import User


class Trainee(User):

    def as_dict(self):
        """Returns all attributes of the Trainee class as a dictionary."""
        return {
            "id": self.id,
            "username": self.username,
            "password": self.password,
            "name": self.name,
            "location": self.location,
            "phone": self.phone
        }
