class Trainer(User):
    def __init__(self, t_time=None, t_focus=None):
        self.t_time = t_time
        self.t_focus = t_focus

    def as_dict(self):
        return {
            "id" : self.id,
            "username" : self.username,
            "password" : self.password,
            "firstname" : self.firstname,
            "lastname" : self.lastname,
            "location" : self.location,
            "phone" : self.phone
            "t_time" : self.t_time
            "t_focus" : self.t_focus
        }

