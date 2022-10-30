
class Config(object):
	"""
	Configuration base, for all environments.
	"""
	DEBUG = False
	TESTING = False
	SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:root@localhost/main'
	BOOTSTRAP_FONTAWESOME = True
	SECRET_KEY = "hello"
	CSRF_ENABLED = True
	SQLALCHEMY_TRACK_MODIFICATIONS = True


class ProductionConfig(Config):
	SQLALCHEMY_DATABASE_URI = 'mysql://user@localhost/foo'
	SQLALCHEMY_TRACK_MODIFICATIONS = False


class DevelopmentConfig(Config):
	DEBUG = True
	TESTING = True


class TestingConfig(Config):
	TESTING = True
