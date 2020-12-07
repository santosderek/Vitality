class Invitation ():

    def __init__(self, _id, sender, recipient):
        self._id = _id
        self.sender = sender
        self.recipient = recipient

    def __repr__(self):
        return f'Invitation({self._id}, {self.sender}, {self.recipient})'
