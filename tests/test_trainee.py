import unittest
from vitality.trainee import Trainee


class TestUser(unittest.TestCase):

    def test_as_dict(self):

        new_user = Trainee(_id=0, username="test", password="password",
                           name="first last", location="Earth", phone=1234567890, trainers=[])

        new_dict = new_user.as_dict()
        comp_dict = {
            "_id": 0,
            "username": "test",
            "password": "password",
            "name": "first last",
            "location": "Earth",
            "phone": 1234567890,
            'trainers': [],
            "body_type": None,
            "body_fat": None,
            "height": None,
            "weight": None,
            "exp": None,
            "goal_weight": None,
            "goal_body_fat": None
        }

        self.assertTrue(new_dict == comp_dict)


if __name__ == '__main__':
    unittest.main()
