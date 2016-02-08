A Python/flask implementation of an openregister, ideal for prototyping data models.

[![Build Status](https://travis-ci.org/openregister/openregister.svg)](https://travis-ci.org/openregister/openregister) [![Coverage Status](https://coveralls.io/repos/openregister/openregister/badge.svg)](https://coveralls.io/r/openregister/openregister)

Pre-requisites
--------------

Uses the [entry]() mongodb as a store.

Setting up
----------

Create and activate a virtualenv:

    virtualenv -p python3 openregister.org
    source openregister.org/bin/activate

Install requirements:

    make init

Set environment variables:

    . environment.sh

Load data:

    make load

Run tests:

    make test

Add the following line to your hosts file on your host machine (you may want to edit this to add new registries):

    127.0.0.1 register.openregister.dev field.openregister.dev tag.openregister.dev datatype.openregister.dev education.openregister.dev

Alternatively setup DNS on your machine to resolve \*.dev to localhost. On Mac OS X you can use [DNSMasq](http://www.toddandrae.com/?p=111)

Run the app:

    ./run_dev.sh

You should now be able to open http://field.openregister.dev:8000/ in a browser.


Deploying
----------

Deployment is to heroku. To deploy, activate the virtualenv, set env variable for HEROKU\_KEY for your heroky api key.

Deployment will be from master of this repository.

Run the management command to deploy an instance of this application to serve a given register name. For example:

```
python manage.py deploy -r registername
```

This command can be used to deploy or redeploy. On first deploy it will create a heroku app with the name "registername-openregister.herokuapp.com" and set a domain name for the application of: "registername.openregister.org".

Once deployed you can load the application with the following command to be run on the heroku application (i.e. wrap the manangement command with heroku run)

For example:

```
heroku run python manage.py --repo-url https://github.com/openregister/field.register --app field-openregister
```

This loads or reloads data. So if new data is added to https://github.com/openregister/field.register, you can run the above again.
