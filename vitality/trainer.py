class Trainer(User):
    def __init__(self, trainees):
        self.trainees = trainees

    def as_dict(self):
        return {
            "id" : self.id,
            "username" : self.username,
            "password" : self.password,
            "firstname" : self.firstname,
            "lastname" : self.lastname,
            "location" : self.location,
            "phone" : self.phone
            "trainees" : self.trainees
        }

    def add_trainee(user_id):
        self.trainees.append(user_id)

    def remove_trainee(user_id):
        self.trainees.remove(user_id)