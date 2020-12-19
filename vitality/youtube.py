from googleapiclient.discovery import build
from time import sleep

class Youtube:

    def __init__(self, developerKey):
        self.youtube = build('youtube', 'v3', developerKey=developerKey)

    def search_topic(self, topic: str):
        sleep(.5)
        request = self.youtube.search().list(
            part="snippet",
            maxResults=6,
            q=topic
        )
        response = request.execute()
        return response

    def __del__(self):
        if hasattr(self, 'youtube'): 
            self.youtube.close()
