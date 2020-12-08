from .user import User


class Trainer(User):
    def __init__(self,
                 trainees=[],
                 **kwargs):
        """Constructor for Trainer."""
        super().__init__(**kwargs)
        self.trainees = trainees

    def __repr__(self):
        return f'Trainer({self._id}, {self.username}, {self.password}, {self.name}, {self.location}, {self.phone}, {self.body_type}, {self.body_fat}, {self.height}, {self.weight}, {self.exp}, {self.goal_weight}, {self.goal_body_fat}, {self.trainees})'
