import os 

#default config
class BaseConfig(object):
	DEBUG = False
	SECRET_KEY = 'xa6\xfb\xb2\x93\x8f\x97p\xd2\xd7\xfb\xc4f\xe8\xf8<\xaaO1\x00V\xd7!\xd4\xf1'
	SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']
	#SQLALCHEMY_DATABASE_URI = "postgresql://postgres:123456@localhost/engramar"

#Development Config
class DevelopmentConfig(BaseConfig):
	DEBUG = True

#Production Config
class ProductionConfig(BaseConfig):
	DEBUG = False