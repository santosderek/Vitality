from os import environ 

SECRET_KEY = environ.get('SECRET_KEY')
MONGO_URI = environ.get('MONGO_URI')
GOOGLE_CLIENT_ID = environ.get('GOOGLE_CLIENT_ID')
GOOGLE_SECRET_ID = environ.get('GOOGLE_SECRET_ID')