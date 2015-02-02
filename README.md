Code for http://thingstance.org

[![Build Status](https://travis-ci.org/thingstance/thingstance.org.svg)](https://travis-ci.org/thingstance/thingstance.org) [![Coverage Status](https://coveralls.io/repos/thingstance/thingstance.org/badge.svg)](https://coveralls.io/r/thingstance/thingstance.org)

Setting up
----------

Create and activate a virtualenv called e.g. `thingstance.org`:

    virtualenv -p python3 thingstance.org
    source thingstance.org/bin/activate

Install requirements:

    make init

Set environment variables:

    . environment.sh

Load data:

    make load

Run tests:

    make test

Add the following line to your hosts file on your host machine (you may want to edit this to add new registries):

    0.0.0.0 register.thingstance.dev field.thingstance.dev tag.thingstance.dev datatype.thingstance.dev education.thingstance.dev

Run the app:

    ./run_dev.sh

You should now be able to open e.g. http://field.thingstance.dev:8000/ in a browser.
