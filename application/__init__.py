import os
import logging

from flask import Flask

app = Flask(__name__)
app.config.from_object(os.environ.get('SETTINGS'))

if not app.debug:
    app.logger.addHandler(logging.StreamHandler())
    app.logger.setLevel(logging.INFO)


# we'll use this handle to db to check collections
# this app can serve.
import pymongo # NOQA
client = pymongo.MongoClient(app.config['MONGO_URI'])
db = client.get_default_database()


from application.views import *  # NOQA
