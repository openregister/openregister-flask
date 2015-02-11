#!/usr/bin/env python3

import os
import sys
import json
import time

import requests

from flask.ext.script import Manager
from application import app
from application.registry import Register, registers

app.config.from_object(os.environ['SETTINGS'])
manager = Manager(app)


@manager.option('-s', '--source', dest='source')
def load_data(source):
    for name in os.listdir(source):
        path = os.path.join(source, name)
        if os.path.isdir(path):
            register = Register(name, app.config['MONGO_URI'])
            register.load(path)

#This should only be run locally, not on heroku. it requires your heroku
#auth token as an environment variable i.e. run HEROKU_KEY=`heroku auth:token`
@manager.option('-r', '--register-name', dest='register_name')
def deploy(register_name):
    heroku_key = "Bearer %s" % os.environ['HEROKU_KEY']
    headers = {"Content-Type" : "application/json",
                "Accept" : "application/vnd.heroku+json; version=3",
                "Authorization" : heroku_key}

    if _exists(register_name, headers):
        _redeploy(register_name, headers)
    else:
        _deploy(register_name, headers)


def _deploy(register_name, headers):
    url = 'https://api.heroku.com/app-setups'
    app_name = "%s-openregister" % register_name
    data = { "app": { "name": app_name, "region": "eu"},
            "source_blob": {
            "url":"https://github.com/openregister/server/tarball/master/" },
            "overrides": {"env": { "REGISTERS": register_name, "REGISTER_DOMAIN": "openregister.org"}}}
    print('deploying register:', app_name)
    resp = requests.post(url, data=json.dumps(data), headers=headers)
    _check_build_status(resp.json(), url)


def _redeploy(register_name, headers):
    app_name = '%s-openregister' % register_name
    url = 'https://api.heroku.com/apps/%s/builds' % app_name
    data =  {"source_blob": {
                "url": "https://github.com/openregister/server/archive/master.tar.gz",
                "version": "v0.1.0"
                }
    }
    print('redeploying', app_name)
    resp = requests.post(url, data=json.dumps(data), headers=headers)
    _check_build_status(resp.json(), url)

def _exists(register_name, headers):
    app_name = '%s-openregister' % register_name
    url = 'https://api.heroku.com/apps/%s' % app_name
    resp = requests.get(url, headers=headers)
    if resp.status_code == 200:
        app_url = resp.json()['web_url']
        print(app_name, 'exists at url:', app_url)
    else:
        print(app_name, 'does not exist')

    return resp.status_code == 200

def _check_build_status(build_response, url):
    build_status = build_response['status']
    build_id = build_response['id']
    print('build status:', build_status)
    print('build id:', build_id)
    if build_status not in ['pending', 'succeeded']:
        print('build error:', build_status, 'message', build['failure_message'])
        sys.exit(1)

    check_url = '%s/%s' % (url, build_id)
    print('check_url:', check_url)
    heroku_key = "Bearer %s" % os.environ['HEROKU_KEY']
    headers = {"Content-Type" : "application/json","Accept" : "application/vnd.heroku+json; version=3", "Authorization" : heroku_key}

    max_poll = 50
    while True and max_poll > 0:
        for i in range(30):
            print('.', end='', flush=True)
            time.sleep(1)
        print('\nchecking build status')
        resp = requests.get(check_url, headers=headers)
        build = resp.json()
        build_status = build['status']
        print('status:', build_status)
        if build_status == 'failed':
            print('build failure:', build['failure_message'])
            sys.exit(1)
        elif build_status == 'succeeded':
            print('build complete')
            app_url = build.get('resolved_success_url')
            if app_url:
                import webbrowser
                webbrowser.open(app_url)
            sys.exit(0)
        max_poll -= 1


if __name__ == '__main__':
    manager.run()
