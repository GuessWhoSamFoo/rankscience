from flask import Flask
from flask_mysqldb import MySQL

application = Flask(__name__, instance_relative_config=True)
mysql = MySQL(application)
application.config.from_object('config.DeploymentConfig')
