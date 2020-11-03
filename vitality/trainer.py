from .user import User


class Trainer(User):
    def __init__(self, id: str, username: str, password: str, trainees: list = None, name: str = None,  location: str = None, phone: int = None):
        """Constructor for Trainer."""
        super().__init__(id, username, password, name,  location, phone)
        self.trainees = trainees

    def as_dict(self):
        """Returns all attributes of the Trainer class and the inherited Trainee class as a dictionary."""
        return {
            **super().as_dict(),
            "trainees": self.trainees
        }