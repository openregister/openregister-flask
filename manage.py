#!/usr/bin/env python3

import os

from flask.ext.script import Manager
from application import app
from application.registry import Register

app.config.from_object(os.environ['SETTINGS'])
manager = Manager(app)


@manager.option('-s', '--source', dest='source')
def load_data(source):
    for name in os.listdir(source):
        path = os.path.join(source, name)
        if os.path.isdir(path):
            register = Register(name=name)
            register.load(path)


if __name__ == '__main__':
    manager.run()
