from datetime import datetime
import unittest
from vitality.event import Event
class TestEvent(unittest.TestCase):
    def test_event(self):

        event = Event("0", "1", datetime(2020, 3, 6), "title", "description")

        assert event._id == "0"
        assert event.creator_id == "1"
        assert event.date == '2020-03-06 00:00:00'
        assert event.title == "title"
        assert event.description == "description"

        event = Event("0", "1", (2020, 3, 6), "title", "description")

        assert event._id == "0"
        assert event.creator_id == "1"
        assert event.date == '2020-03-06 00:00:00'
        assert event.title == "title"
        assert event.description == "description"


    def test_as_dict(self):

        new_event = Event(_id="0", creator_id="1", date=datetime(2020, 3, 6), title="title", description="description")

        new_dict = new_event.as_dict()
        comp_dict = {
            "_id": "0",
            "creator_id": "1",
            "date": 'datetime(2020, 3, 6)',
            "title": "title",
            "description": "description"
        }
        self.assertTrue(new_dict == comp_dict)



    def test_invitation_repr(self):

        event = Event("0", "1", datetime(2020, 3, 6), "title", "description")

        assert repr(event) \
            == 'Event(0, 1, 2020-03-06 00:00:00, title, description)'