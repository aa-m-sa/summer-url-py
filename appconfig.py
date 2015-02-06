# the app config

class Config(object):

    """Different configuration settings subclassed from this"""

    DATABASE = 'insert heroku postgres db here'
    DEBUG = False

class DevelopmentConfig(Config):
    DEBUG = True

class ProductionConfig(Config):
    DATABASE = 'insert production db here'
