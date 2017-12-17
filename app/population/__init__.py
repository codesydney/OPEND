#from flask import Flask, g, request, make_response, redirect, url_for, jsonify, render_template
from flask import Blueprint

"""
import csv
import os
import os.path
import glob
import json
import traceback
"""

#UPLOAD_FOLDER = './data/'
#ALLOWED_EXTENSIONS = set(['csv'])

#app = Flask(__name__,static_url_path='')
#app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

population = Blueprint(
    'population',
    __name__,
    template_folder='templates',
    static_folder='static'
)

from . import views

#if __name__ == '__main__':
#    app.run(debug=True)