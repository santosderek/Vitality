import unittest
from vitality.trainer import Trainer


class TestTrainer(unittest.TestCase):

    def test_as_dict(self):

        new_trainer = Trainer(
            _id="0",
            username="test",
            password="password",
            trainees=[],
            name="first last",
            location="Earth",
            phone=1234567890
        )

        new_dict = new_trainer.as_dict()
        comp_dict = {
            "_id": "0",
            "username": "test",
            "password": "password",
            "trainees": [],
            "name": "first last",
            "location": "Earth",
            "phone": 1234567890,
            "body_type": None,
            "body_fat": None,
            "height": None,
            "weight": None,
            "exp": None,
            "goal_weight": None,
            "goal_body_fat": None
        }

        self.assertTrue(new_dict == comp_dict)
