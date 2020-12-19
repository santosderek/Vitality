from vitality.youtube import *
from os import environ, getenv
from os.path import exists
from vitality.settings import GOOGLE_MAPS_KEY
from dotenv import load_dotenv 
from time import sleep
import pytest 

@pytest.mark.skip
def test_search_topic():
    sleep(.5)
    load_dotenv('.env')
    youtube = Youtube(getenv("GOOGLE_YOUTUBE_KEY"))
    response = youtube.search_topic('Low Carb Recipe')
    assert len(response) == 6
    assert 'items' in response
    assert 'etag' in response

    # from pprint import pprint
    # pprint (response)
    # assert False

def test_fallback_dicts():
    assert 'kind' in DEFAULT_YOUTUBE_WORKOUT_SEARCH
    assert 'etag' in DEFAULT_YOUTUBE_WORKOUT_SEARCH
    assert 'nextPageToken' in DEFAULT_YOUTUBE_WORKOUT_SEARCH
    assert 'regionCode' in DEFAULT_YOUTUBE_WORKOUT_SEARCH
    assert 'pageInfo' in DEFAULT_YOUTUBE_WORKOUT_SEARCH

    assert 'kind' in DEFAULT_YOUTUBE_DIET_SEARCH
    assert 'etag' in DEFAULT_YOUTUBE_DIET_SEARCH
    assert 'nextPageToken' in DEFAULT_YOUTUBE_DIET_SEARCH
    assert 'regionCode' in DEFAULT_YOUTUBE_DIET_SEARCH
    assert 'pageInfo' in DEFAULT_YOUTUBE_DIET_SEARCH