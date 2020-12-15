import unittest
from vitality.trainer import Trainer


def test_as_dict():

    trainer = Trainer(
        _id="000000000000000000000001",
        username="trainer",
        password="newPassword",
        name="test trainer",
        location="mars",
        phone="1234567890",
        body_type="big",
        body_fat="fat",
        height="7",
        weight="100",
        exp=12345,
        goal_weight="95",
        goal_body_fat="notfat",
        trainees=[
            "000000000000000000000002"
        ]
    )

    new_dict = trainer.as_dict()
    comp_dict = dict(
        _id="000000000000000000000001",
        username="trainer",
        password="newPassword",
        name="test trainer",
        location="mars",
        phone="1234567890",
        body_type="big",
        body_fat="fat",
        height="7",
        weight="100",
        exp=12345,
        goal_weight="95",
        goal_body_fat="notfat",
        trainees=[
            "000000000000000000000002"
        ]
    )

    assert new_dict == comp_dict


def test_initalization():
    trainer = Trainer(
        _id="000000000000000000000001",
        username="trainer",
        password="newPassword",
        name="test trainer",
        location="mars",
        phone="1234567890",
        body_type="big",
        body_fat="fat",
        height="7",
        weight="100",
        exp=12345,
        goal_weight="95",
        goal_body_fat="notfat",
        trainees=[
            "000000000000000000000002"
        ]
    )

    assert trainer._id == '000000000000000000000001'
    assert trainer.username == 'trainer'
    assert trainer.password == "newPassword"
    assert trainer.name == "test trainer"
    assert trainer.location == "mars"
    assert trainer.phone == "1234567890"
    assert trainer.body_type == "big"
    assert trainer.body_fat == "fat"
    assert trainer.height == "7"
    assert trainer.weight == "100"
    assert trainer.exp == 12345
    assert trainer.goal_weight == "95"
    assert trainer.goal_body_fat == "notfat"
    assert trainer.trainees == ["000000000000000000000002"]


def test_repr():
    trainer = Trainer(
        _id="000000000000000000000001",
        username="trainer",
        password="newPassword",
        name="test trainer",
        location="mars",
        phone="1234567890",
        body_type="big",
        body_fat="fat",
        height="7",
        weight="100",
        exp="12345",
        goal_weight="95",
        goal_body_fat="notfat",
        trainees=[
            "000000000000000000000002"
        ]
    )

    assert repr(
        trainer) == "Trainer(000000000000000000000001, trainer, newPassword, test trainer, mars, 1234567890, big, fat, 7, 100, 12345, 95, notfat, [\'000000000000000000000002\'])"
