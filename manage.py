#!/usr/bin/env python3

import os

from flask.ext.script import Manager
from application import app
from application import mongo

app.config.from_object(os.environ['SETTINGS'])
manager = Manager(app)

@manager.option('-s', '--source', dest='source')
def load_data(source):
    from data.things import ThingLoader
    loader = ThingLoader(source, mongo)
    loader.load_json()

@manager.command
def drop_db():
    mongo.db.connection.drop_database('things')


if __name__ == '__main__':
    manager.run()
