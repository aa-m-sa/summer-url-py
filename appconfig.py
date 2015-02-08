# the app config
import os

class Config(object):

    """Different configuration settings subclassed from this"""

    DATABASE_URL = 'insert devel url here'
    DEBUG = False

class DevelopmentConfig(Config):
    DEBUG = True
    DATABASE_URL = os.environ.get("SUMMER_DEV_DATABASE_URL")

class ProductionConfig(Config):
    DATABASE_URL = os.environ.get("DATABASE_URL")

class TestConfig(Config):
    DATABASE_URL = os.environ.get("SUMMER_TEST_DATABASE_URL")
    TESTING = True
