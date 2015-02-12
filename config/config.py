import os

class Config(object):
    DEBUG = False
    REGISTER_DOMAIN=os.environ['REGISTER_DOMAIN']
    MONGO_URI = os.environ.get('MONGOLAB_URI', 'mongodb://127.0.0.1:27017/thingstance')
    PAGE_SIZE = int(os.environ['PAGE_SIZE'])
    SECRET_KEY = os.environ['SECRET_KEY']

class DevelopmentConfig(Config):
    DEBUG = True

class TestConfig(DevelopmentConfig):
    TESTING = True
