from .user import User


class Trainee(User):
    def __init__(self, _id: str, username: str, password: str, name: str = None, location: str = None, phone: int = None, trainers=[]):
        super().__init__(
            _id=_id,
            username=username,
            password=password,
            name=name,
            location=location,
            phone=phone
        )
        self.trainers = trainers
        
    def as_dict(self):
        """Returns all attributes of the Trainer class and the inherited Trainee class as a dictionary."""
        return {
            **super().as_dict(),
            "trainers": self.trainers
        }
