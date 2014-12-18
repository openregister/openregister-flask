import os
import logging

from flask import Flask
from flask.ext.pymongo import PyMongo

app = Flask(__name__)
app.config.from_object(os.environ.get('SETTINGS'))

mongo = PyMongo(app)

from application.views import *

if not app.debug:
    app.logger.addHandler(logging.StreamHandler())
    app.logger.setLevel(logging.INFO)
