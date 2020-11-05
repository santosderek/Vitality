import json


class Configuration ():

    def __init__(self, path: str = 'configuration.json'):
        """Constructor for Configuration class. Grabs configuration.json file."""
        self.__data = {}

        with open(path, 'r') as current_file:
            self.__data = json.loads(current_file.read())

    def get_local_uri(self):
        """Returns the URI for the local mongo database."""
        return self.__data['mongodb']['localuri']

    def get_atlas_uri(self):
        """Returns the URI for the Atlas stored database."""
        return self.__data['mongodb']['atlasuri']

    def get_googlemaps_client_id(self):
        """Returns the client id for the google maps API."""
        return self.__data['googlemaps']['client_id']

    def get_googlemaps_client_secret(self):
        """Returns the client secret for the google maps API."""
        return self.__data['googlemaps']['client_secret']

    def get_youtube_client_id(self):
        """Returns the client id for the youtube API."""
        return self.__data['youtube']['client_id']

    def get_youtube_client_secret(self):
        """Returns the client secret for the youtube API."""
        return self.__data['youtube']['client_secret']
