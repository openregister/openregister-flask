Code for http://thingstance.org

https://travis-ci.org/openregister/server.svg?branch=master

[![Build Status](https://travis-ci.org/openregister/server.svg)](https://travis-ci.org/openregister/server) [![Coverage Status](https://coveralls.io/repos/thingstance/thingstance.org/badge.svg)](https://coveralls.io/r/thingstance/thingstance.org)

Pre-requisites
--------------
Local running mongodb

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


Deploying
----------

Deployment is to heroku. To deploy, activate the virtualenv, set env variable for HEROKU_KEY for your heroky api key.

Deployement will be from master of this repository.

Run the managment command to deploy an instance of this application to serve a given register name. For example:

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


