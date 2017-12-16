from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap

import os

app = Flask(__name__)
#app.config.from_object("config")
app.config.from_object(os.environ['APP_SETTINGS'])
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db = SQLAlchemy(app)

bootstrap = Bootstrap(app)

#importing main must be after db = SQLAlchemy(app)
from .main import main

app.register_blueprint(main,url_prefix='/main')
