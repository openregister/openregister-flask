#!/bin/bash

source /home/ubuntu/environment.sh

./bin/gunicorn -c bin/gunicorn_config.py application.views:app
