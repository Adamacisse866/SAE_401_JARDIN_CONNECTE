import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = 'secret_key_here'
    SQLALCHEMY_DATABASE_URI = 'mysql://username:password@localhost/db_name'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SOCKETIO_BROKER_URL = 'redis://localhost:6379'
    SOCKETIO_REDIS_URL = 'redis://localhost:6379'
    MAPBOX_ACCESS_TOKEN = 'mapbox_access_token_here'
    PLANT_ID_API_KEY = 'plant_id_api_key_here'
    WEB_PUSH_API_KEY = 'web_push_api_key_dsfe'