import unittest
from vitality.user import User


def test_as_dict():

    user = User(
        _id="000000000000000000000001",
        username="user",
        password="newPassword",
        name="test user",
        phone="1234567890",
        body_type="big",
        body_fat="fat",
        height="7",
        weight="100",
        exp=12345,
        goal_weight="95",
        goal_body_fat="notfat",
        lng=0,
        lat=0
    )

    new_dict = user.as_dict()
    comp_dict = dict(
        _id="000000000000000000000001",
        username="user",
        password="newPassword",
        name="test user",
        phone="1234567890",
        body_type="big",
        body_fat="fat",
        height="7",
        weight="100",
        exp=12345,
        goal_weight="95",
        goal_body_fat="notfat",
        lng=0,
        lat=0
    )

    assert new_dict == comp_dict


def test_initalization():
    user = User(
        _id="000000000000000000000001",
        username="user",
        password="newPassword",
        name="test user",
        phone="1234567890",
        body_type="big",
        body_fat="fat",
        height="7",
        weight="100",
        exp="12345",
        goal_weight="95",
        goal_body_fat="notfat",
        lng=0,
        lat=0
    )

    assert user._id == '000000000000000000000001'
    assert user.username == 'user'
    assert user.password == "newPassword"
    assert user.name == "test user"
    assert user.phone == "1234567890"
    assert user.body_type == "big"
    assert user.body_fat == "fat"
    assert user.height == "7"
    assert user.weight == "100"
    assert user.exp == 12345
    assert user.goal_weight == "95"
    assert user.goal_body_fat == "notfat"
    assert user.lng == 0
    assert user.lat == 0


def test_repr():
    user = User(
        _id="000000000000000000000001",
        username="user",
        password="newPassword",
        name="test user",
        phone="1234567890",
        body_type="big",
        body_fat="fat",
        height="7",
        weight="100",
        exp="12345",
        goal_weight="95",
        goal_body_fat="notfat",
        lng="0",
        lat="0"
    )

    assert repr(user) \
        == "User(000000000000000000000001, user, newPassword, test user, 1234567890, big, fat, 7, 100, 12345, 95, notfat, 0, 0)"


if __name__ == '__main__':
    unittest.main()
