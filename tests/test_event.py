from datetime import datetime
import unittest
from vitality.event import Event
class TestEvent(unittest.TestCase):
    def test_event(self):

        event = Event("0", "1", datetime(2020, 3, 6), "title", "description", participant_id="0000000000000001")

        assert event._id == "0"
        assert event.creator_id == "1"
        assert str(event.date) == '2020-03-06 00:00:00'
        assert event.title == "title"
        assert event.description == "description"
        assert event.participant_id == "0000000000000001"

        event = Event("0", "1", (2020, 3, 6), "title", "description", participant_id="0000000000000002")

        assert event._id == "0"
        assert event.creator_id == "1"
        assert str(event.date) == '2020-03-06 00:00:00'
        assert event.title == "title"
        assert event.description == "description"
        assert event.participant_id == "0000000000000002"


    def test_as_dict(self):

        new_event = Event(_id="0", creator_id="1", date=datetime(2020, 3, 6), title="title", description="description", participant_id="0000000000000001")

        new_dict = new_event.as_dict()
        comp_dict = {
            "_id": "0",
            "creator_id": "1",
            "date": "2020-03-06 00:00:00",
            "title": "title",
            "description": "description",
            "participant_id": "0000000000000001"
        }
        self.assertTrue(new_dict == comp_dict)



    def test_invitation_repr(self):

        event = Event("0", "1", datetime(2020, 3, 6), "title", "description", "0000000000000000")

        assert repr(event) \
            == 'Event(0, 1, 2020-03-06 00:00:00, title, description, 0000000000000000)'