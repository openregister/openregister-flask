import os
import logging

from flask import Flask

app = Flask(__name__)
app.config.from_object(os.environ.get('SETTINGS'))

from application.views import *  # NOQA

if not app.debug:
    app.logger.addHandler(logging.StreamHandler())
    app.logger.setLevel(logging.INFO)
