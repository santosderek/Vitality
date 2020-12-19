from vitality.youtube import *
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

def test_fallback_dicts():
    assert 'kind' in DEFAULT_FALL_BACK_WORKOUT_DICT
    assert 'etag' in DEFAULT_FALL_BACK_WORKOUT_DICT
    assert 'nextPageToken' in DEFAULT_FALL_BACK_WORKOUT_DICT
    assert 'regionCode' in DEFAULT_FALL_BACK_WORKOUT_DICT
    assert 'pageInfo' in DEFAULT_FALL_BACK_WORKOUT_DICT