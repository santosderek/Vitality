import unittest
from vitality.trainer import Trainer

class TestTrainer(unittest.TestCase):

    def test_as_dict(self):

        new_trainer = Trainer(0,"test", "password", "None", "first", "last", "Earth", 1234567890)

        new_dict = new_trainer.as_dict()
        comp_dict = {
            "id" : 0,
            "username" : "test",
            "password" : "password",
            "trainees" : "None",
            "firstname" : "first",
            "lastname" : "last",
            "location" : "Earth",
            "phone" : 1234567890
            }

        self.assertTrue(new_dict == comp_dict)


if __name__ == '__main__':
    unittest.main()