from dotenv import load_dotenv 
from os import environ

load_dotenv('.env')

SECRET_KEY = environ.get('SECRET_KEY')
MONGO_URI = environ.get('MONGO_URI')
GOOGLE_MAPS_KEY = environ.get('GOOGLE_MAPS_KEY')
GOOGLE_YOUTUBE_KEY = environ.get('GOOGLE_YOUTUBE_KEY')
