class User:
    def __init__(self, id, username, password, location=None, phone=None):
        self.id = id
        self.username = username
        self.password = password
        self.location = location
        self.phone = phone
