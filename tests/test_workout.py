import unittest
from vitality.workout import Workout


def test_as_dict():

    workout = Workout(
        _id="000000000000000000000001",
        creator_id="000000000000000000000002",
        name="Workout 1",
        difficulty="easy",
        about="An about section",
        is_complete=False
    )

    new_dict = workout.as_dict()
    comp_dict = dict(
        _id="000000000000000000000001",
        creator_id="000000000000000000000002",
        name="Workout 1",
        difficulty="easy",
        about="An about section",
        is_complete=False
    )

    assert new_dict == comp_dict


def test_initalization():
    workout = Workout(
        _id="000000000000000000000001",
        creator_id="000000000000000000000002",
        name="Workout 1",
        difficulty="easy",
        about="An about section",
        is_complete=False
    )

    assert workout._id == "000000000000000000000001"
    assert workout.creator_id == "000000000000000000000002"
    assert workout.name == "Workout 1"
    assert workout.difficulty == "easy"
    assert workout.about == "An about section"
    assert workout.is_complete == False


def test_repr():
    workout = Workout(
        _id="000000000000000000000001",
        creator_id="000000000000000000000002",
        name="Workout 1",
        difficulty="easy",
        about="An about section",
        is_complete=False
    )

    assert repr(workout) \
        == "Workout(000000000000000000000001, 000000000000000000000002, Workout 1, easy, An about section, False)"


if __name__ == '__main__':
    unittest.main()
