import unittest
from vitality.trainee import Trainee

class TestUser(unittest.TestCase):

    def test_as_dict(self):

        new_user = Trainee(0,"test", "password", "first last", "Earth", 1234567890, trainers=[])

        new_dict = new_user.as_dict()
        comp_dict = {
            "_id" : 0,
            "username" : "test",
            "password" : "password",
            "name": "first last",
            "location" : "Earth",
            "phone" : 1234567890, 
            'trainers' : [] 
            }

        self.assertTrue(new_dict == comp_dict)


if __name__ == '__main__':
    unittest.main()