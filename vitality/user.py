class User:
    def __init__(self, id, username, password, name=None, location=None, phone=None):
        """Constructor for Trainee class."""
        self.id = id
        self.username = username
        self.password = password
        self.name = name
        self.location = location
        self.phone = phone
    
    def as_dict(self):
        """Returns all attributes of the Trainee class as a dictionary."""
        return {
            "_id" : self.id,
            "username" : self.username,
            "password" : self.password,
            "name": self.name, 
            "location" : self.location,
            "phone" : self.phone
        }