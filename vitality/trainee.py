from .user import User


class Trainee(User):
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
                 goal_body_fat: str = None,
                 trainers=[]):
        """Constructor for Trainer."""
        super().__init__(_id,
                         username,
                         password,
                         name,
                         location,
                         phone,
                         body_type,
                         body_fat,
                         height,
                         weight,
                         exp,
                         goal_weight,
                         goal_body_fat)
        self.trainers = trainers
