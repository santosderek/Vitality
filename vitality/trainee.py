from .user import User


class Trainee(User):
    def __init__(self, trainers=[], **kwargs):
        """Constructor for Trainer."""
        super().__init__(**kwargs)
        self.trainers = trainers

    def __repr__(self):
        return f'Trainee({self._id}, {self.username}, {self.password}, {self.name}, {self.location}, {self.phone}, {self.body_type}, {self.body_fat}, {self.height}, {self.weight}, {self.exp}, {self.goal_weight}, {self.goal_body_fat}, {self.trainers})'
