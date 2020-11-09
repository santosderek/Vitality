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
