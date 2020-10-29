class User:
    def __init__(self, id, username, password, firstname=None, lastname=None, location=None, phone=None):
        """Constructor for Trainee class."""
        self.id = id
        self.username = username
        self.password = password
        self.firstname = firstname
        self.lastname = lastname
        self.location = location
        self.phone = phone
    
    def as_dict(self):
        """Returns all attributes of the Trainee class as a dictionary."""
        return {
            "_id" : self.id,
            "username" : self.username,
            "password" : self.password,
            "firstname" : self.firstname,
            "lastname" : self.lastname,
            "location" : self.location,
            "phone" : self.phone
        }