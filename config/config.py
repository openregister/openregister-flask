import os

class Config(object):
    DEBUG = False
    REGISTER_DOMAIN=os.environ['REGISTER_DOMAIN']
    MONGO_URI = os.environ.get('MONGOLAB_URI', 'mongodb://127.0.0.1:27017/thingstance')
    PAGE_SIZE = int(os.environ['PAGE_SIZE'])
    SECRET_KEY = os.environ['SECRET_KEY']
    GITHUB_ORG = os.environ['GITHUB_ORG']

class DevelopmentConfig(Config):
    DEBUG = True

class DockerConfig(DevelopmentConfig):
    # this is not a good idea as linked container may not be
    # up yet and therefore DB_PORT_27017_TCP_ADDR not yet set
    MONGO_URI = 'mongodb://%s:27017/thingstance' % os.environ.get('DB_PORT_27017_TCP_ADDR')

class TestConfig(DevelopmentConfig):
    TESTING = True
