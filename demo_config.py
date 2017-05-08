# rankscience/__init__.py

class BaseConfig(object):
    DEBUG = False
    MYSQL_USER = 'user'
    MYSQL_PASSWORD = '1234'
    MYSQL_DB = 'exampledb'
    MYSQL_HOST = 'localhost'

class TestingConfig(BaseConfig):
    DEBUG = True

class DeploymentConfig(BaseConfig):
    DEBUG = False
    MYSQL_USER = 'aws_user'
    MYSQL_PASSWORD = '5678'
    MYSQL_DB = 'aws_db'
    MYSQL_HOST = 'aws_endpoint'

