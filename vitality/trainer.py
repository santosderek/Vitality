from .user import User


class Trainer(User):
    def __init__(self, _id: str, username: str, password: str, trainees: list = [], name: str = None,  location: str = None, phone: int = None):
        """Constructor for Trainer."""
        super().__init__(_id, username, password, name,  location, phone)
        self.trainees = trainees
