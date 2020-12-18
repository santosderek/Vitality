from vitality.youtube import Youtube
from os import environ
from vitality.settings import GOOGLE_MAPS_KEY
import pytest

youtube = Youtube('')

@pytest.mark.skip()
def test_search_topic():

    response = youtube.search_topic('fish')

    assert len(response) == 6