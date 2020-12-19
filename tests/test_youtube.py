from vitality.youtube import Youtube
from os import environ, getenv
from os.path import exists
from vitality.settings import GOOGLE_MAPS_KEY
from dotenv import load_dotenv 
from time import sleep
import pytest 

# @pytest.mark.skip
def test_search_topic():
    sleep(.5)
    load_dotenv('.env')
    youtube = Youtube(getenv("GOOGLE_YOUTUBE_KEY"))
    response = youtube.search_topic('fish')
    assert len(response) == 6
    assert 'items' in response
    assert 'etag' in response