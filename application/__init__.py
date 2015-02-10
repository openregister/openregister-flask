import os
import logging

from flask import Flask

app = Flask(__name__)
app.config.from_object(os.environ.get('SETTINGS'))

from application.views import *  # NOQA

if not app.debug:
    app.logger.addHandler(logging.StreamHandler())
    app.logger.setLevel(logging.INFO)


# TBD: load registers from the register register
from .registry import Register
for name in ['Register',
             'Country',
             'Company',
             'Address',
             'Court',
             'School',
             'Datatype',
             'Field',
             'Instrument',
             'Measurement']:
    Register(name, app.config['MONGO_URI'])
