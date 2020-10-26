import unittest
from vitality.user import User

class TestUser(unittest.TestCase):

    def test_as_dict(self):

        new_user = User(0,"test", "password", "first", "last", "Earth", 1234567890)

        new_dict = new_user.as_dict()
        comp_dict = {
            "id" : 0,
            "username" : "test",
            "password" : "password",
            "firstname" : "first",
            "lastname" : "last",
            "location" : "Earth",
            "phone" : 1234567890
            }

        self.assertTrue(new_dict == comp_dict)


if __name__ == '__main__':
    unittest.main()