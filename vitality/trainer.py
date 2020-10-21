from .user import User
class Trainer(User):
    def __init__(self, id, username, password, trainees=None, firstname=None, lastname=None, location=None, phone=None):
        super().__init__(id, username, password, firstname, lastname, location, phone)
        self.trainees = trainees

    def as_dict(self):
        return {
            **super().as_dict(),
            "trainees" : self.trainees
        }

    def add_trainee(user_id):
        self.trainees.append(user_id)

    def remove_trainee(user_id):
        self.trainees.remove(user_id)
