# openregister-flask

[![Build Status](https://travis-ci.org/openregister/openregister-flask.svg)](https://travis-ci.org/openregister/openregister-flask) [![Coverage Status](https://coveralls.io/repos/openregister/openregister-flask/badge.svg)](https://coveralls.io/r/openregister/openregister-flask)

A single [flask](http://flask.pocoo.org/) application intended for prototyping registers.

## Databases and other configuration

Registers are stored in [MongoDB](https://www.mongodb.org/) but can this be changed on a per-register basis to use one of the other stores supported by the [openregister-python](https://pypi.python.org/pypi/openregister/) package by changing the [config.py](config/config.py) file or setting environment variables in [environment.sh](environment.sh), your ``~/.profile``, [Heroku configuration](https://devcenter.heroku.com/articles/config-vars) etc.

## Virtual environment

We recommend using a [Python virtual environment](http://virtualenvwrapper.readthedocs.org/en/latest/):

    $ mkvirtualenv -p python3 myproject
    $ workon myproject

## Package dependencies

    $ make init

## Running

    $ make test
    $ make server

## Supporting multiple registers

Each register is served on its own dedicated host, so you will need to add a hostname for each
register in your ``/etc/hosts`` file, eg:

    127.0.0.1 field.openregister.dev register.openregister.dev datatype.openregister.dev foo.openregister.dev

Alternatively you can setup DNS on your machine to resolve \*.dev to localhost.
On Mac OS X you can use [DNSMasq](http://www.toddandrae.com/?p=111)

You should now be able to open http://field.openregister.dev:8000/ in a browser.
