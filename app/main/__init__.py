import os

from flask import Blueprint
#from flask_sqlalchemy import SQLAlchemy

#main = Flask(__name__)
main = Blueprint(
    'main',
    __name__,
    template_folder='templates',
    static_folder='static'
)


#app.config.from_object('config')
#main.config.from_object(os.environ['APP_SETTINGS'])
#db = SQLAlchemy(main)

from . import views, models