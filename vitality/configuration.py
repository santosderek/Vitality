import json

class Configuration (): 

    def __init__(self, path = 'configuration.json'): 
        self.__data = {}

        with open(path, 'r') as current_file:
            self.__data = json.loads( current_file.read() )

    def get_mongodb_uri(self):
        return self.__data['mongodb']['uri']

    def get_googlemaps_client_id(self):
        return self.__data['googlemaps']['client_id']

    def get_googlemaps_client_secret(self):
        return self.__data['googlemaps']['client_secret']

    def get_youtube_client_id(self):
        return self.__data['youtube']['client_id']

    def get_youtube_client_secret(self):
        return self.__data['youtube']['client_secret']