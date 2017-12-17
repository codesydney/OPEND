from flask import Blueprint

birthrate = Blueprint(
    'birthrate',
    __name__,
    template_folder='templates',
    static_folder='static'
)

from . import views
