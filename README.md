Code for http://thingstance.org

https://travis-ci.org/openregister/server.svg?branch=master

[![Build Status](https://travis-ci.org/openregister/server.svg)](https://travis-ci.org/openregister/server) [![Coverage Status](https://coveralls.io/repos/thingstance/thingstance.org/badge.svg)](https://coveralls.io/r/thingstance/thingstance.org)

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

Alternatively setup DNS on your machine to resolve \*.dev to localhost using something like [DNSMasq](http://www.toddandrae.com/?p=111)

Run the app:

    ./run_dev.sh

You should now be able to open e.g. http://field.thingstance.dev:8000/ in a browser.
