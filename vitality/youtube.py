import requests

YOUTUBE_SEARCH_URL = 'https://www.googleapis.com/youtube/v3/search'


class Youtube:

    def __init__(self, developerKey):
        self.developerKey = developerKey

    def search_topic(self, topic: str):

        returned_value = requests.get(YOUTUBE_SEARCH_URL,
                                      headers={
                                          'Accept': 'application/json'
                                      },
                                      params={
                                          'part': "snippet",
                                          'maxResults': 6,
                                          'q': topic,
                                          'key': self.developerKey
                                      })

        if returned_value.status_code == 200: 
            return returned_value.json()
        else:
           raise YoutubeRequestFailed('Status == {}'.format(returned_value.status_code))

class YoutubeRequestFailed(Exception): 
    pass 