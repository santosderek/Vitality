from .user import User
class Trainer(User):
    def __init__(self, id, username, password, trainees=None, firstname=None, lastname=None, location=None, phone=None):
        """Constructor for Trainer."""
        super().__init__(id, username, password, firstname, lastname, location, phone)
        self.trainees = trainees

    def as_dict(self):
        """Returns all attributes of the Trainer class and the inherited User class as a dictionary."""
        return {
            **super().as_dict(),
            "trainees" : self.trainees
        }

    def add_trainee(self, user_id):
        """Adds the trainee's user id to Trainer's list of trainees."""
        self.trainees.append(user_id)

    def remove_trainee(self, user_id):
        """Removes a trainee's user id to Trainer's list of trainees."""
        self.trainees.remove(user_id)
