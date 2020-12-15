import unittest
from vitality.trainee import Trainee


def test_as_dict():

    trainee = Trainee(
        _id="000000000000000000000001",
        username="trainee",
        password="newPassword",
        name="test trainee",
        location="mars",
        phone="1234567890",
        body_type="big",
        body_fat="fat",
        height="7",
        weight="100",
        exp=12345,
        goal_weight="95",
        goal_body_fat="notfat",
        trainers=[
            "000000000000000000000002"
        ]
    )

    new_dict = trainee.as_dict()
    comp_dict = dict(
        _id="000000000000000000000001",
        username="trainee",
        password="newPassword",
        name="test trainee",
        location="mars",
        phone="1234567890",
        body_type="big",
        body_fat="fat",
        height="7",
        weight="100",
        exp=12345,
        goal_weight="95",
        goal_body_fat="notfat",
        trainers=[
            "000000000000000000000002"
        ]
    )

    assert new_dict == comp_dict


def test_initalization():
    trainee = Trainee(
        _id="000000000000000000000001",
        username="trainee",
        password="newPassword",
        name="test trainee",
        location="mars",
        phone="1234567890",
        body_type="big",
        body_fat="fat",
        height="7",
        weight="100",
        exp=12345,
        goal_weight="95",
        goal_body_fat="notfat",
        trainers=[
            "000000000000000000000002"
        ]
    )

    assert trainee._id == '000000000000000000000001'
    assert trainee.username == 'trainee'
    assert trainee.password == "newPassword"
    assert trainee.name == "test trainee"
    assert trainee.location == "mars"
    assert trainee.phone == "1234567890"
    assert trainee.body_type == "big"
    assert trainee.body_fat == "fat"
    assert trainee.height == "7"
    assert trainee.weight == "100"
    assert trainee.exp == 12345
    assert trainee.goal_weight == "95"
    assert trainee.goal_body_fat == "notfat"
    assert trainee.trainers == ["000000000000000000000002"]


def test_repr():
    trainee = Trainee(
        _id="000000000000000000000001",
        username="trainee",
        password="newPassword",
        name="test trainee",
        location="mars",
        phone="1234567890",
        body_type="big",
        body_fat="fat",
        height="7",
        weight="100",
        exp="12345",
        goal_weight="95",
        goal_body_fat="notfat",
        trainers=[
            "000000000000000000000002"
        ]
    )

    assert repr(trainee) \
        == "Trainee(000000000000000000000001, trainee, newPassword, test trainee, mars, 1234567890, big, fat, 7, 100, 12345, 95, notfat, [\'000000000000000000000002\'])"


if __name__ == '__main__':
    unittest.main()
