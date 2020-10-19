class User:
    def __init__(self, id, username, password, firstname=None, lastname=None, location=None, phone=None):
        self.id = id
        self.username = username
        self.password = password
        self.firstname = firstname
        self.lastname = lastname
        self.location = location
        self.phone = phone
    
    